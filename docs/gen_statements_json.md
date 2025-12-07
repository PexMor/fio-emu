# Generátor JSON výpisů FIO banky

Nástroj `fiocli` umožňuje generovat realistické JSON výpisy bankovních transakcí ve formátu FIO Banking API. Generátor vytváří semi-náhodné hodnoty s minimálním vstupem a umožňuje specifikovat další pravidla pro lepší výstup.

## Instalace

Nástroj je součástí balíčku `fioemu` a je dostupný po instalaci závislostí:

```bash
uv sync
```

## Základní použití

### Minimální příklad

Nejjednodušší způsob použití generuje 10 náhodných transakcí za posledních 30 dní:

```bash
uv run fiocli
```

### Specifikace časového rozsahu

```bash
uv run fiocli --date-from 2024-01-01 --date-to 2024-01-31
```

### Specifikace počtu transakcí

```bash
uv run fiocli --num-transactions 50
```

### Specifikace rozsahu částek

```bash
uv run fiocli --min-amount -5000 --max-amount 10000
```

### Kompletní příklad s všemi parametry

```bash
uv run fiocli \
  --account-id 2400222222 \
  --bank-id 2010 \
  --currency CZK \
  --date-from 2024-01-01 \
  --date-to 2024-01-31 \
  --num-transactions 25 \
  --min-amount -5000 \
  --max-amount 10000 \
  --opening-balance 1000.0 \
  --output statement.json \
  --pretty
```

## Parametry

### `--account-id`

Číslo účtu (10 číslic). Pokud není zadáno, generuje se náhodně.

**Příklad:**

```bash
uv run fiocli --account-id 2400222222
```

### `--bank-id`

Kód banky. Pokud není zadáno, vybere se náhodně z běžných českých bank:

- `2010` - Fio banka
- `0800` - Česká spořitelna
- `0100` - Komerční banka
- `2700` - UniCredit Bank
- `5500` - Raiffeisenbank
- `0600` - Moneta Money Bank

**Příklad:**

```bash
uv run fiocli --bank-id 2010
```

### `--currency`

Kód měny (výchozí: `CZK`).

**Příklad:**

```bash
uv run fiocli --currency EUR
```

### `--date-from`

Počáteční datum ve formátu `YYYY-MM-DD`. Pokud není zadáno, použije se datum před 30 dny.

**Příklad:**

```bash
uv run fiocli --date-from 2024-01-01
```

### `--date-to`

Koncové datum ve formátu `YYYY-MM-DD`. Pokud není zadáno, použije se dnešní datum.

**Příklad:**

```bash
uv run fiocli --date-to 2024-01-31
```

### `--num-transactions`

Počet transakcí k vygenerování (výchozí: `10`).

**Příklad:**

```bash
uv run fiocli --num-transactions 50
```

### `--min-amount`

Minimální částka transakce. Pokud není zadáno, výchozí hodnota je `-10000.0`.

**Příklad:**

```bash
uv run fiocli --min-amount -5000
```

### `--max-amount`

Maximální částka transakce. Pokud není zadáno, výchozí hodnota je `10000.0`.

**Příklad:**

```bash
uv run fiocli --max-amount 10000
```

### `--opening-balance`

Počáteční zůstatek na účtu. Pokud není zadáno, výchozí hodnota je `0.0`. Konečný zůstatek se automaticky vypočítá na základě transakcí.

**Příklad:**

```bash
uv run fiocli --opening-balance 1000.0
```

### `--output`

Cesta k výstupnímu souboru. Pokud není zadáno, výstup se zobrazí na standardním výstupu.

**Příklad:**

```bash
uv run fiocli --output statement.json
```

### `--pretty`

Formátuje JSON výstup s odsazením pro lepší čitelnost.

**Příklad:**

```bash
uv run fiocli --pretty
```

## Generované hodnoty

Generátor automaticky vytváří realistické hodnoty pro:

### Transakce

- **ID pohybu**: Unikátní číselné ID pro každou transakci
- **Datum**: Náhodné datum v zadaném rozsahu
- **Objem**: Částka v zadaném rozsahu (může být kladná i záporná)
- **Měna**: Podle parametru `--currency`
- **Typ transakce**: Náhodně vybraný z běžných typů:
  - Příjem převodem uvnitř banky
  - Platba převodem uvnitř banky
  - Příjem převodem z jiné banky
  - Platba převodem do jiné banky
  - Připsaný úrok
  - Připsaná provize
  - Inkaso
  - Trvalý příkaz
  - SIPO
  - Kartová transakce
  - Výběr z bankomatu
  - Vklad hotovosti

### Protiúčet (pokud je relevantní)

- **Číslo protiúčtu**: Náhodně vygenerované 10místné číslo
- **Kód banky**: Náhodně vybraný z běžných českých bank
- **Název banky**: Název odpovídající kódu banky
- **Název protiúčtu**: Realistické české jméno ve formátu "Příjmení, Jméno"
- **KS (Konstantní symbol)**: Standardní hodnota `0558`
- **Uživatelská identifikace**: Někdy prázdné, někdy variabilní symbol
- **Proved1**: Někdy jméno osoby, která provedla transakci
- **Komentář**: Někdy prázdný, někdy popis transakce

### Informace o účtu

- **IBAN**: Automaticky vygenerovaný z kódu banky a čísla účtu
- **BIC**: Automaticky vygenerovaný podle kódu banky
- **ID pokynu**: Unikátní ID pro každou transakci
- **dateStart/dateEnd**: Automaticky vypočítané z transakcí
- **idFrom/idTo**: Automaticky vypočítané z ID transakcí
- **idLastDownload**: ID poslední stažené transakce

## Příklady použití

### Generování výpisu pro testování

```bash
# Generovat 20 transakcí za leden 2024
uv run fiocli \
  --date-from 2024-01-01 \
  --date-to 2024-01-31 \
  --num-transactions 20 \
  --output january_statement.json \
  --pretty
```

### Generování výpisu s konkrétním účtem

```bash
# Generovat výpis pro konkrétní účet Fio banky
uv run fiocli \
  --account-id 2400222222 \
  --bank-id 2010 \
  --date-from 2024-01-01 \
  --date-to 2024-01-31 \
  --num-transactions 15 \
  --opening-balance 5000.0 \
  --output fio_statement.json \
  --pretty
```

### Generování výpisu pouze s příjmy

```bash
# Generovat pouze kladné transakce
uv run fiocli \
  --min-amount 0 \
  --max-amount 50000 \
  --num-transactions 10 \
  --output income_statement.json \
  --pretty
```

### Generování výpisu pouze s výdaji

```bash
# Generovat pouze záporné transakce
uv run fiocli \
  --min-amount -50000 \
  --max-amount 0 \
  --num-transactions 10 \
  --output expenses_statement.json \
  --pretty
```

## Integrace s emulátorem

Vygenerovaný JSON lze použít s emulátorem FIO API:

1. **Vygenerujte výpis:**

   ```bash
   uv run fiocli --output statement.json --pretty
   ```

2. **Nahrajte výpis do emulátoru:**

   ```bash
   curl -X POST http://localhost:8000/emu/v1/periods \
     -H "Content-Type: application/json" \
     -d @statement.json
   ```

3. **Získejte filtrovaný výpis:**
   ```bash
   curl "http://localhost:8000/v1/rest/periods/token/2024-01-01/2024-01-15/transactions.json"
   ```

## Struktura výstupu

Výstupní JSON odpovídá struktuře FIO Banking API v1.9:

```json
{
  "accountStatement": {
    "info": {
      "accountId": "2400222222",
      "bankId": "2010",
      "currency": "CZK",
      "iban": "CZ7920100000002400222222",
      "bic": "FIOBCZPPXXX",
      "openingBalance": 0.0,
      "closingBalance": 195.01,
      "dateStart": 1340661600000,
      "dateEnd": 1341007200000,
      "yearList": null,
      "idList": null,
      "idFrom": 1148734530,
      "idTo": 1149190193,
      "idLastDownload": 1149190192
    },
    "transactionList": {
      "transaction": [
        {
          "column22": { "value": 1148734530, "name": "ID pohybu", "id": 22 },
          "column0": { "value": 1340661600000, "name": "Datum", "id": 0 },
          "column1": { "value": 1.0, "name": "Objem", "id": 1 },
          ...
        }
      ]
    }
  }
}
```

## Poznámky

- Transakce jsou automaticky seřazeny podle data
- Konečný zůstatek se automaticky vypočítá z počátečního zůstatku a všech transakcí
- Datumy jsou ve formátu timestamp v milisekundách (Unix epoch)
- Všechny částky jsou zaokrouhleny na 2 desetinná místa
- Generátor používá realistická česká jména a názvy bank
- Některá pole mohou být `null` v závislosti na typu transakce
