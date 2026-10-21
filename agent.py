"""Offline AI Companion — single-file application core.

Stage 12–20 implementation scaffold.
The file intentionally contains the core runtime in one place. External model
weights and persistent user data stay outside the repository.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sqlite3
import sys
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Optional


# ============================================================
# CONFIGURATION
# ============================================================

APP_NAME = "Offline AI Companion"
APP_VERSION = "0.1.0"
DEFAULT_MODEL = "qwen3.5:4b"
FALLBACK_MODEL = "qwen3.5:2b"
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 11434
DEFAULT_DB_NAME = "memory.sqlite3"


@dataclass
class Config:
    """Runtime configuration with safe local defaults."""

    model: str = DEFAULT_MODEL
    host: str = DEFAULT_HOST
    port: int = DEFAULT_PORT
    database: str = DEFAULT_DB_NAME
    temperature: float = 0.8
    context_limit: int = 8192
    stream: bool = True
    debug: bool = False

    @property
    def base_url(self) -> str:
        return f"http://{self.host}:{self.port}"

    @classmethod
    def from_file(cls, path: Path) -> "Config":
        if not path.exists():
            return cls()
        data = json.loads(path.read_text(encoding="utf-8"))
        allowed = {field for field in cls.__dataclass_fields__}
        return cls(**{k: v for k, v in data.items() if k in allowed})

    def save(self, path: Path) -> None:
        path.write_text(
            json.dumps(asdict(self), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )


# ============================================================
# LOGGING
# ============================================================


def configure_logging(debug: bool = False) -> logging.Logger:
    logger = logging.getLogger(APP_NAME)
    if logger.handlers:
        return logger
    logger.setLevel(logging.DEBUG if debug else logging.INFO)
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
    logger.addHandler(handler)
    return logger


LOGGER = configure_logging()


# ============================================================
# LOCAL STORAGE / MEMORY
# ============================================================


class MemoryStore:
    """Small SQLite layer for local sessions and explicit memories."""

    def __init__(self, database_path: Path):
        self.path = database_path
        self.connection: Optional[sqlite3.Connection] = None

    def connect(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(self.path)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.connection.execute("PRAGMA journal_mode = WAL")
        self.initialize()

    def initialize(self) -> None:
        if self.connection is None:
            raise RuntimeError("MemoryStore is not connected")
        self.connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at REAL NOT NULL,
                title TEXT
            );

            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at REAL NOT NULL,
                FOREIGN KEY(session_id) REFERENCES sessions(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT NOT NULL,
                value TEXT NOT NULL,
                importance REAL NOT NULL DEFAULT 0.5,
                created_at REAL NOT NULL,
                updated_at REAL NOT NULL
            );
            """
        )
        self.connection.commit()

    def create_session(self, title: str = "Conversation") -> int:
        if self.connection is None:
            raise RuntimeError("MemoryStore is not connected")
        cursor = self.connection.execute(
            "INSERT INTO sessions(created_at, title) VALUES(?, ?)",
            (time.time(), title),
        )
        self.connection.commit()
        return int(cursor.lastrowid)

    def add_message(self, session_id: int, role: str, content: str) -> None:
        if self.connection is None:
            raise RuntimeError("MemoryStore is not connected")
        self.connection.execute(
            "INSERT INTO messages(session_id, role, content, created_at) VALUES(?, ?, ?, ?)",
            (session_id, role, content, time.time()),
        )
        self.connection.commit()

    def recent_messages(self, session_id: int, limit: int = 20) -> list[dict[str, str]]:
        if self.connection is None:
            raise RuntimeError("MemoryStore is not connected")
        rows = self.connection.execute(
            "SELECT role, content FROM messages WHERE session_id=? ORDER BY id DESC LIMIT ?",
            (session_id, limit),
        ).fetchall()
        return [dict(row) for row in reversed(rows)]

    def remember(self, key: str, value: str, importance: float = 0.5) -> None:
        if self.connection is None:
            raise RuntimeError("MemoryStore is not connected")
        now = time.time()
        self.connection.execute(
            "INSERT INTO memories(key, value, importance, created_at, updated_at) VALUES(?, ?, ?, ?, ?)",
            (key, value, float(importance), now, now),
        )
        self.connection.commit()

    def memories(self, limit: int = 20) -> list[dict[str, Any]]:
        if self.connection is None:
            raise RuntimeError("MemoryStore is not connected")
        rows = self.connection.execute(
            "SELECT id, key, value, importance, created_at, updated_at "
            "FROM memories ORDER BY importance DESC, updated_at DESC LIMIT ?",
            (limit,),
        ).fetchall()
        return [dict(row) for row in rows]

    def close(self) -> None:
        if self.connection is not None:
            self.connection.close()
            self.connection = None


# ============================================================
# PERSONA
# ============================================================


@dataclass
class Persona:
    name: str = "Nova"
    role: str = "offline AI companion"
    tone: str = "warm, natural, friendly, lightly humorous"
    language: str = "auto"
    system_rules: str = (
        "Be conversational and consistent. Do not pretend to have experiences "
        "or abilities that you do not have. Keep the user's privacy local."
    )

    def system_prompt(self) -> str:
        return (
            f"You are {self.name}, an {self.role}.\n"
            f"Tone: {self.tone}.\n"
            f"Preferred language: {self.language}.\n"
            f"Rules: {self.system_rules}\n"
        )


# ============================================================
# MODEL ADAPTER
# ============================================================


class ModelAdapter:
    """Interface boundary for a local model runtime.

    The initial runtime is Ollama's local HTTP API. The implementation uses
    only the Python standard library so the companion can start without an
    additional SDK; if Ollama is unavailable, the program reports a clear
    offline-runtime error instead of silently using a cloud service.
    """

    def __init__(self, config: Config):
        self.config = config

    def generate(self, messages: list[dict[str, str]]) -> str:
        try:
            import urllib.error
            import urllib.request
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError("Python HTTP support is unavailable") from exc

        payload = json.dumps(
            {
                "model": self.config.model,
                "messages": messages,
                "stream": False,
                "options": {"temperature": self.config.temperature},
            }
        ).encode("utf-8")
        request = urllib.request.Request(
            f"{self.config.base_url}/api/chat",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=600) as response:
                data = json.loads(response.read().decode("utf-8"))
        except urllib.error.URLError as exc:
            raise RuntimeError(
                "Local model runtime is unavailable. Start Ollama locally "
                f"and make sure model '{self.config.model}' is installed."
            ) from exc

        message = data.get("message", {})
        content = message.get("content")
        if not isinstance(content, str):
            raise RuntimeError("Local model returned an invalid response")
        return content


# ============================================================
# CONVERSATION ENGINE
# ============================================================


class ConversationEngine:
    def __init__(self, config: Config, memory: MemoryStore, persona: Persona):
        self.config = config
        self.memory = memory
        self.persona = persona
        self.model = ModelAdapter(config)
        self.session_id: Optional[int] = None

    def start(self) -> int:
        if self.session_id is None:
            self.session_id = self.memory.create_session()
        return self.session_id

    def build_messages(self, user_text: str) -> list[dict[str, str]]:
        if self.session_id is None:
            self.start()
        history = self.memory.recent_messages(self.session_id, limit=20)
        remembered = self.memory.memories(limit=10)
        memory_text = "\n".join(
            f"- {item['key']}: {item['value']}" for item in remembered
        ) or "(no stored memories)"
        messages = [{"role": "system", "content": self.persona.system_prompt()}]
        messages.append(
            {
                "role": "system",
                "content": "Relevant local memories:\n" + memory_text,
            }
        )
        messages.extend(history)
        messages.append({"role": "user", "content": user_text})
        return messages

    def respond(self, user_text: str) -> str:
        if not user_text.strip():
            return ""
        session_id = self.start()
        self.memory.add_message(session_id, "user", user_text)
        response = self.model.generate(self.build_messages(user_text))
        self.memory.add_message(session_id, "assistant", response)
        return response


# ============================================================
# CLI
# ============================================================


def default_data_directory() -> Path:
    override = os.environ.get("OFFLINE_AI_HOME")
    if override:
        return Path(override).expanduser()
    return Path.home() / ".offline_ai_companion"


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=APP_NAME)
    parser.add_argument("--model", default=None)
    parser.add_argument("--data-dir", default=str(default_data_directory()))
    parser.add_argument("--config", default=None)
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--version", action="version", version=APP_VERSION)
    return parser.parse_args(argv)


def build_config(args: argparse.Namespace) -> Config:
    config_path = Path(args.config) if args.config else Path(args.data_dir) / "config.json"
    config = Config.from_file(config_path)
    if args.model:
        config.model = args.model
    if args.debug:
        config.debug = True
    configure_logging(config.debug)
    return config


def run_cli(config: Config, data_dir: Path) -> int:
    data_dir.mkdir(parents=True, exist_ok=True)
    config_path = data_dir / "config.json"
    if not config_path.exists():
        config.save(config_path)

    memory = MemoryStore(data_dir / config.database)
    memory.connect()
    persona = Persona()
    engine = ConversationEngine(config, memory, persona)

    print(f"{APP_NAME} {APP_VERSION}")
    print(f"Model: {config.model} | Local runtime: {config.base_url}")
    print("Type /help for commands. Type /exit to quit.")

    try:
        while True:
            try:
                user_text = input("You: ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                break
            if not user_text:
                continue
            if user_text == "/exit":
                break
            if user_text == "/help":
                print("/help  show commands\n/exit  quit\n/memory  show local memories")
                continue
            if user_text == "/memory":
                items = memory.memories()
                if not items:
                    print("Memory: empty")
                else:
                    for item in items:
                        print(f"- {item['key']}: {item['value']}")
                continue
            try:
                print("AI: " + engine.respond(user_text))
            except RuntimeError as exc:
                print(f"AI runtime error: {exc}")
    finally:
        memory.close()
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    args = parse_args(argv)
    config = build_config(args)
    return run_cli(config, Path(args.data_dir).expanduser())


if __name__ == "__main__":
    raise SystemExit(main())
