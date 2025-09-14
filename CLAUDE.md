# Project Conventions

## Python Package Management

- **Use `uv` for all package management** (not pip)
- Add dependencies: `uv add package-name`
- Install project: `uv install`

## Code Quality

- No backwards compatibility - keep scripts simple
- Line length: 88 characters max
- Use type hints and assertions for regex matches
- Auto-fix mode preferred over validation-only
- Use pyright for typing.
- Use ruff for formatting and linting.
- Do not use type: ignore or t.Any unless there is no way around.
