# Vývojový průvodce

## Nastavení

### Předpoklady

- Python 3.13+
- Správce balíčků [uv](https://github.com/astral-sh/uv)

### Počáteční nastavení

```bash
# Instalace závislostí
uv sync

# Toto provede:
# - Vytvoření virtuálního prostředí
# - Instalaci všech závislostí
# - Instalaci balíčku fioemu v editovatelném režimu
```

## Spuštění aplikace

### Prostřednictvím uv

```bash
# Přímé spuštění
uv run fioemu

# Spuštění s argumenty
uv run fioemu --host 0.0.0.0 --port 8080

# Spuštění jako modul
uv run python -m fioemu
```

### Proměnné prostředí

```bash
export FIOEMU_HOST=0.0.0.0
export FIOEMU_PORT=8080
uv run fioemu
```

## Struktura projektu

```
fioemu/
├── __init__.py
├── __main__.py          # Vstupní bod a registrace routerů
├── app.py               # Factory pro FastAPI aplikaci
├── config.py            # Správa konfigurace
├── utils.py             # Pomocné funkce
└── routers/             # Handlery API rout
    ├── __init__.py
    ├── periods/         # GET /v1/rest/periods/{token}/{date_from}/{date_to}/transactions.{format}
    ├── by_id/           # GET /v1/rest/by-id/{token}/{year}/{id}/transactions.{format}
    ├── last/             # GET /v1/rest/last/{token}/transactions.{format}
    ├── set_last_id/      # GET /v1/rest/set-last-id/{token}/{id}/
    ├── set_last_date/    # GET /v1/rest/set-last-date/{token}/{date}/
    ├── merchant/         # GET /v1/rest/merchant/{token}/{date_from}/{date_to}/transactions.{format}
    ├── last_statement/   # GET /v1/rest/lastStatement/{token}/statement
    └── import_/         # POST /v1/rest/import/
```

## Přidávání nových routů

1. Vytvořte novou podsložku v `fioemu/routers/`
2. Vytvořte `__init__.py` s definicí routeru:

```python
from fastapi import APIRouter

router = APIRouter(prefix="/v1/rest/your-endpoint", tags=["your-tag"])

@router.get("/{token}/transactions.{format}")
async def your_handler(token: str, format: str):
    # Implementace
    pass
```

3. Importujte a zahrňte router v `fioemu/__main__.py`:

```python
from fioemu.routers import your_router

app.include_router(your_router.router)
```

4. Přidejte příklady odpovědí do `~/.config/fioemu/examples/<router-name>/`

## Testování

Aplikace automaticky generuje OpenAPI dokumentaci na:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

## Závislosti

Klíčové závislosti:
- **fastapi**: Webový framework
- **uvicorn**: ASGI server
- **pydantic**: Validace dat pomocí Python type hints
- **pydantic-settings**: Správa nastavení pro Pydantic
- **pyyaml**: YAML parser
- **tomli**: TOML parser (pro Python < 3.11)
- **python-multipart**: Vyžadováno pro nahrávání souborů

Viz `pyproject.toml` pro kompletní seznam závislostí.

## Styl kódu

- Dodržujte stylový průvodce PEP 8
- Používejte type hints pro všechny signatury funkcí
- Dokumentujte funkce a třídy pomocí docstringů
- Udržujte funkce zaměřené a modulární
