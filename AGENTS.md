# Průvodce technickou architekturou

Tento dokument poskytuje přehled architektury a klíčových technických rozhodnutí pro FIO Banking API Emulator. Pro podrobné průvodce implementací viz [Vývojový průvodce](docs/DEVELOPMENT.md) a [Průvodce konfigurací](docs/CONFIGURATION.md).

## Přehled architektury

FIO Banking API Emulator je aplikace založená na FastAPI, která emuluje FIO Banking API v1.9. Používá modulární routerovou architekturu pro udržovatelnost a rozšiřitelnost.

## Klíčová technická rozhodnutí

### Správa balíčků: uv

**Rozhodnutí**: Použití `uv` pro správu balíčků místo pip/poetry.

**Odůvodnění**:
- Rychlý instalátor a resolver Python balíčků napsaný v Rustu
- Lepší výkon při řešení závislostí
- Moderní nástroje v souladu s požadavky Python 3.13+
- Zjednodušený workflow s `uv sync` a `uv run`

**Odkaz**: Viz [Vývojový průvodce](docs/DEVELOPMENT.md) pro instrukce k nastavení.

### Webový framework: FastAPI

**Rozhodnutí**: Použití FastAPI jako webového frameworku.

**Odůvodnění**:
- Vysoký výkon (srovnatelný s Node.js a Go)
- Automatická dokumentace API (OpenAPI/Swagger)
- Vestavěné type hints a validace Pydantic
- Moderní podpora Python async/await
- Vynikající vývojářský zážitek

**Použité funkce**:
- Routerová architektura pro modulární organizaci endpointů
- Automatické generování OpenAPI dokumentace
- CORS middleware pro cross-origin požadavky
- Podpora nahrávání souborů (multipart/form-data)

### Správa konfigurace: Multi-source priorita

**Rozhodnutí**: Podpora více zdrojů konfigurace s jasným pořadím priority.

**Odůvodnění**:
- Flexibilita pro různé scénáře nasazení
- Vhodné pro vývoj (CLI argumenty) i produkci (env vars/config soubory)
- Dodržuje principy 12-factor app

**Pořadí priority**:
1. Argumenty příkazové řádky
2. Proměnné prostředí (`FIOEMU_*`)
3. Konfigurační soubory (YAML/TOML)
4. Výchozí hodnoty

**Odkaz**: Viz [Průvodce konfigurací](docs/CONFIGURATION.md) pro podrobnosti.

### Routerová architektura: Modulární struktura

**Rozhodnutí**: Organizace routů v samostatných modulech, jeden router na skupinu endpointů.

**Odůvodnění**:
- Jasné oddělení zodpovědností
- Snadné nalezení a úprava konkrétních endpointů
- Podpora nezávislého vývoje a testování
- Dobře škáluje s růstem API

**Struktura**:
```
fioemu/routers/
├── periods/          # Dotazy na časové období
├── by_id/            # Výpis podle ID
├── last/              # Poslední transakce
├── set_last_id/       # Nastavení checkpointu podle ID
├── set_last_date/     # Nastavení checkpointu podle data
├── merchant/          # Karetní transakce
├── last_statement/     # Číslo posledního výpisu
└── import_/           # Nahrávání platebních příkazů
```

Každý router modul:
- Definuje svou vlastní instanci `APIRouter`
- Obsahuje route handlery pro danou skupinu endpointů
- Může být nezávisle vyvíjen a testován

**Odkaz**: Viz [Vývojový průvodce](docs/DEVELOPMENT.md) pro přidávání nových routů.

## API Endpointy

Emulátor implementuje všechny endpointy z FIO API v1.9:

### GET Endpointy
- `/v1/rest/periods/{token}/{date_from}/{date_to}/transactions.{format}` - Dotazy na časové období
- `/v1/rest/by-id/{token}/{year}/{id}/transactions.{format}` - Oficiální výpisy
- `/v1/rest/last/{token}/transactions.{format}` - Od posledního stažení
- `/v1/rest/set-last-id/{token}/{id}/` - Nastavení checkpointu podle ID
- `/v1/rest/set-last-date/{token}/{date}/` - Nastavení checkpointu podle data
- `/v1/rest/merchant/{token}/{date_from}/{date_to}/transactions.{format}` - Karetní transakce
- `/v1/rest/lastStatement/{token}/statement` - Číslo posledního výpisu

### POST Endpointy
- `/v1/rest/import/` - Nahrávání platebních příkazů (abo, xml, pain001xml, pain008xml)

**Odkaz**: Viz [API Dokumentace](docs/API_docs_1_9.md) pro kompletní referenci API.

## Systém příkladových odpovědí

Příklady odpovědí jsou uloženy v `~/.config/fioemu/examples/` podle strukturované konvence pojmenování:
- Formát: `<api-id>_<number>.<format>`
- Organizováno podle názvu routeru (odpovídá skupinám API endpointů)
- Podporuje více scénářů na endpoint

**Odkaz**: Viz [Průvodce konfigurací](docs/CONFIGURATION.md) pro strukturu adresáře s příklady.

## Závislosti

Hlavní závislosti:
- **fastapi**: Webový framework
- **uvicorn**: ASGI server
- **pydantic**: Validace dat
- **pydantic-settings**: Správa nastavení
- **pyyaml**: Parsování YAML konfigurace
- **tomli**: Parsování TOML konfigurace
- **python-multipart**: Podpora nahrávání souborů

**Odkaz**: Viz `pyproject.toml` pro kompletní seznam závislostí.

## Vývojový workflow

1. **Nastavení**: `uv sync` pro instalaci závislostí
2. **Spuštění**: `uv run fioemu` pro spuštění serveru
3. **Testování**: Použití Swagger UI na `http://localhost:8000/docs`
4. **Vývoj**: Přidávání routů podle modulárního routerového vzoru

**Odkaz**: Viz [Vývojový průvodce](docs/DEVELOPMENT.md) pro podrobný workflow a pokyny pro přispívání.
