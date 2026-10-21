# Stage 13 — Configuration

## Goal
Centralize runtime settings without scattering constants through the application.

## Implemented
`agent.py` contains the `Config` dataclass with:
- model name
- local host/port
- database filename
- temperature
- context limit
- streaming flag
- debug flag

Configuration can be loaded from a local JSON file and saved as a local default. The data directory can be selected with `--data-dir` or `OFFLINE_AI_HOME`.

## Privacy
Configuration is local. It is not uploaded by the application.

## Exit criteria
A fresh run can construct configuration with safe defaults and override the model/data directory from the command line.
