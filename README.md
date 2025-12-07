# FIO Emulator

Tento software je inspirován a snaží se co nejvěrněji vycházet z dokumentace FIO Banking API.

Jeho oficiální popis je dostupný na <https://www.fio.cz/docs/cz/API_Bankovnictvi.pdf> v době psaní tohoho dokumentu (**7.prosince 2025**) byla platná verze `1.9`.

Smyslem tohoto repozitáře je převod původního dokumentu určeného pro tisk je vytvoření alternativního formátu (*markdown*), se kterým se snáze pracuje a dovoluje přirozenější vkládání příkladů.

Samotný převod **PDF** na **Markdown** je v [docs/API_docs_1_9.md](docs/API_docs_1_9.md).

## Rychlý start

### Instalace

```bash
uv sync
```

### Spuštění

```bash
uv run fioemu
```

API bude dostupné na <http://localhost:8000> s interaktivní dokumentací na:
- Swagger UI: <http://localhost:8000/docs>
- ReDoc: <http://localhost:8000/redoc>

### Konfigurace

Konfigurace může být poskytnuta prostřednictvím:
- Argumentů příkazové řádky (`--host`, `--port`)
- Proměnných prostředí (`FIOEMU_HOST`, `FIOEMU_PORT`)
- Konfiguračních souborů (`~/.config/fioemu/config.yaml` nebo `config.toml`)

Více informací najdete v [docs/CONFIGURATION.md](docs/CONFIGURATION.md).

## Dokumentace

- **[Architektura a vývojový průvodce](AGENTS.md)** - Technický přehled a vývojové pokyny
- **[API Reference](docs/API_docs_1_9.md)** - Kompletní dokumentace FIO API (v1.9)
- **[Konfigurace](docs/CONFIGURATION.md)** - Podrobnosti o správě konfigurace
- **[Vývoj](docs/DEVELOPMENT.md)** - Nastavení vývojového prostředí a pokyny pro přispívání

## Stav projektu

Tento projekt je v aktivním vývoji. Historie verzí je v [CHANGELOG.md](CHANGELOG.md).
