# Průvodce konfigurací

FIO Banking API Emulator podporuje konfiguraci z více zdrojů s následující prioritou (od nejvyšší po nejnižší):

1. **Argumenty příkazové řádky** (`--host`, `--port`, atd.)
2. **Proměnné prostředí** (s prefixem `FIOEMU_`, např. `FIOEMU_HOST`, `FIOEMU_PORT`)
3. **Konfigurační soubory**:
   - YAML: `~/.config/fioemu/config.yaml`
   - TOML: `~/.config/fioemu/config.toml` (fallback pokud YAML neexistuje)
4. **Výchozí hodnoty** (definované ve třídě `Config`)

## Umístění konfiguračních souborů

Konfigurační soubory jsou uloženy v adresáři `~/.config/fioemu/`.

## Formáty konfigurace

### YAML formát (preferovaný)

Vytvořte `~/.config/fioemu/config.yaml`:

```yaml
host: "127.0.0.1"
port: 8000
cors_origins:
  - "*"
cors_allow_credentials: true
cors_allow_methods:
  - GET
  - POST
cors_allow_headers:
  - "*"
```

### TOML formát

Vytvořte `~/.config/fioemu/config.toml`:

```toml
host = "127.0.0.1"
port = 8000
cors_origins = ["*"]
cors_allow_credentials = true
cors_allow_methods = ["GET", "POST"]
cors_allow_headers = ["*"]
```

## Proměnné prostředí

Všechny konfigurační možnosti mohou být nastaveny prostřednictvím proměnných prostředí s prefixem `FIOEMU_`:

```bash
export FIOEMU_HOST=0.0.0.0
export FIOEMU_PORT=8080
export FIOEMU_CORS_ORIGINS='["*"]'
export FIOEMU_CORS_ALLOW_CREDENTIALS=true
```

## Argumenty příkazové řádky

```bash
uv run fioemu --host 0.0.0.0 --port 8080
```

Dostupné argumenty:
- `--host`: Host pro navázání připojení
- `--port`: Port pro navázání připojení
- `--config-dir`: Vlastní adresář konfigurace (výchozí: `~/.config/fioemu`)
- `--examples-dir`: Vlastní adresář příkladů (výchozí: `config_dir/examples`)

## Adresář příkladů

Příklady odpovědí jsou uloženy v `~/.config/fioemu/examples/` podle této struktury:

```
~/.config/fioemu/examples/
├── periods/
│   ├── periods_1.xml
│   ├── periods_1.json
│   └── periods_2.xml
├── by_id/
│   ├── by_id_1.xml
│   └── by_id_1.json
└── ...
```

Konvence pojmenování: `<api-id>_<number>.<format>`

Kde:
- `<api-id>` odpovídá názvu podsložky routeru
- `<number>` je pořadové číslo pro různé scénáře odpovědí
- `<format>` je formát odpovědi (xml, json, csv, atd.)
