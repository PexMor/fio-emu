# Changelog

Všechny významné změny v tomto projektu budou zdokumentovány v tomto souboru.

Formát je založen na [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
a tento projekt dodržuje [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Nevydáno]

### Přidáno
- Počáteční struktura projektu s emulátorem založeným na FastAPI
- Routerová architektura pro modulární organizaci endpointů
- Podpora více zdrojů konfigurace (CLI argumenty, env proměnné, config soubory)
- Podpora všech endpointů FIO API v1.9:
  - GET endpointy: periods, by-id, last, set-last-id, set-last-date, merchant, last-statement
  - POST endpoint: import (platební příkazy)
- Systém příkladových odpovědí s konfigurovatelným adresářem příkladů
- Podpora CORS middleware
- Automatická dokumentace OpenAPI/Swagger

### Změněno
- Struktura dokumentace reorganizována pro lepší udržovatelnost

## [0.1.0] - 2025-12-07

### Přidáno
- Počáteční vydání
- Základní implementace emulátoru FIO Banking API
- Integrace frameworku FastAPI
- Nastavení správy balíčků uv
