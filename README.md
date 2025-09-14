# Arma Ukraine Reforger

Collection of Arma Reforger mods for Ukraine-themed gameplay.

## Modules

- **AUADeadEveron** - Dead Everon scenario
- **AUADeadEveronDeltaT** - Delta variant of Dead Everon
- **AUAFFPlusTweaks** - Freedom Fighters tweaks

## Development

```bash
# Setup
python -m venv .venv
uv add pre-commit ruff pyright

# Install hooks
uv run pre-commit install

# Validate prices
python AUAFFPlusTweaks/validate_prices.py --fix
```

Pre-commit hooks automatically validate configuration files and code quality.
