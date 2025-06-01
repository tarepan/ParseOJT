# ParseOJT
Parser of Open JTalk text-processing output (NJD features).

```mermaid
graph TD;
    A["Open JTalk NJD features"] --> B["Utterance"];
    B --> C["VOICEVOX AccentPhrases"];
    B --> D["visual graph"];
```

## Dev
### All-in Check
```bash
## check-and-fix
uv run mypy . && uv run ruff check --fix && uv run ruff format && uv run typos && uv run pytest
```

### All-in Static Program Analysis
```bash
# check-only
uv run mypy . && uv run ruff check && uv run ruff format --check && uv run typos

## check-and-fix
uv run mypy . && uv run ruff check --fix && uv run ruff format && uv run typos
```