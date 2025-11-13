# RTCCFD 🔎

## Prerequisites
- Python 3.12+
- [uv](https://docs.astral.sh/uv/getting-started/installation/) package manager
- [GitGuardian ggshield](https://docs.gitguardian.com/ggshield-docs/getting-started) for secret scanning

## Setup Instructions

### 1. Install dev dependencies and pre-commit hooks

**Linux/macOS:**
```bash
make install-hooks
```

**Windows (PowerShell/CMD):**
```powershell
uv sync --group dev
uv run pre-commit install
```

### 2. GitGuardian Setup 

**Install ggshield:**

- **macOS:**
  ```bash
  brew install gitguardian/tap/ggshield
  ```

- **Linux/Windows:**
  ```bash
  pip install ggshield
  # or
  pipx install ggshield
  ```

**First-time authentication:**
```bash
ggshield auth login
```

**Skip if not using:** Pre-commit will still work, but ggshield hooks will be skipped.


## Troubleshooting

- **ggshield not found**: Install it or remove from `.pre-commit-config.yaml`
- **Windows make errors**: Use the manual PowerShell commands instead
- **Permission denied**: On Linux/macOS, you may need `chmod +x` for scripts