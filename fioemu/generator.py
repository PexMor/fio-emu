"""
Common module for generating random FIO bank statement JSON responses.

This module is used by both the CLI (`fiocli`) and the API (`/emu/v1/generate`).
"""

import random
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

# Czech names for realistic account names
CZECH_FIRST_NAMES = [
    "Jan",
    "Petr",
    "Pavel",
    "Tomáš",
    "Martin",
    "Jiří",
    "Lukáš",
    "Michal",
    "Jakub",
    "David",
    "Marie",
    "Jana",
    "Petra",
    "Eva",
    "Anna",
    "Hana",
    "Lenka",
    "Kateřina",
    "Lucie",
    "Alena",
]

CZECH_LAST_NAMES = [
    "Novák",
    "Svoboda",
    "Novotný",
    "Dvořák",
    "Černý",
    "Procházka",
    "Veselý",
    "Horák",
    "Němec",
    "Pospíšil",
    "Hájek",
    "Král",
    "Jelínek",
    "Růžička",
    "Beneš",
    "Fiala",
    "Sedláček",
    "Doležal",
    "Zeman",
    "Kolář",
]

BANK_NAMES = [
    "Fio banka, a.s.",
    "Česká spořitelna, a.s.",
    "Komerční banka, a.s.",
    "UniCredit Bank Czech Republic and Slovakia, a.s.",
    "Raiffeisenbank a.s.",
    "Moneta Money Bank, a.s.",
]

TRANSACTION_TYPES = [
    "Příjem převodem uvnitř banky",
    "Platba převodem uvnitř banky",
    "Příjem převodem z jiné banky",
    "Platba převodem do jiné banky",
    "Připsaný úrok",
    "Připsaná provize",
    "Inkaso",
    "Trvalý příkaz",
    "SIPO",
    "Kartová transakce",
    "Výběr z bankomatu",
    "Vklad hotovosti",
]

BANK_CODES = ["2010", "0800", "0100", "2700", "5500", "0600"]


class StatementGenerationParams(BaseModel):
    """Parameters for generating a FIO bank statement."""

    account_id: Optional[str] = Field(
        default=None, description="Account ID (10 digits, default: random)"
    )
    bank_id: Optional[str] = Field(
        default=None, description="Bank code (default: random from common Czech banks)"
    )
    currency: str = Field(default="CZK", description="Currency code (default: CZK)")
    date_from: Optional[str] = Field(
        default=None, description="Start date in YYYY-MM-DD format (default: 30 days ago)"
    )
    date_to: Optional[str] = Field(
        default=None, description="End date in YYYY-MM-DD format (default: today)"
    )
    num_transactions: int = Field(
        default=10, ge=0, le=1000, description="Number of transactions to generate (default: 10)"
    )
    min_amount: Optional[float] = Field(
        default=None, description="Minimum transaction amount (default: -10000)"
    )
    max_amount: Optional[float] = Field(
        default=None, description="Maximum transaction amount (default: 10000)"
    )
    opening_balance: Optional[float] = Field(
        default=None, description="Opening balance (default: 0.0)"
    )


def generate_account_id() -> str:
    """Generate a random Czech account ID (10 digits)."""
    return "".join([str(random.randint(0, 9)) for _ in range(10)])


def generate_iban(bank_id: str, account_id: str) -> str:
    """Generate IBAN from bank ID and account ID."""
    return f"CZ{bank_id}000000{account_id}"


def generate_bic(bank_id: str) -> str:
    """Generate BIC code from bank ID."""
    bank_bics = {
        "2010": "FIOBCZPPXXX",
        "0800": "GIBACZPX",
        "0100": "KOMBCZPP",
        "2700": "BACXCZPP",
        "5500": "RZBCCZPP",
        "0600": "AGBACZPX",
    }
    return bank_bics.get(bank_id, "FIOBCZPPXXX")


def generate_timestamp(date_from: datetime, date_to: datetime) -> int:
    """Generate a random timestamp in milliseconds between date_from and date_to."""
    delta = date_to - date_from
    random_days = random.randint(0, max(0, delta.days))
    random_seconds = random.randint(0, 86400 - 1)
    random_date = date_from + timedelta(days=random_days, seconds=random_seconds)
    return int(random_date.timestamp() * 1000)


def generate_transaction_id(base_id: int, index: int) -> int:
    """Generate a transaction ID."""
    return base_id + index * random.randint(100, 1000)


def generate_order_id(base_id: int, index: int) -> int:
    """Generate an order ID."""
    return base_id + index * random.randint(50, 500)


def generate_vs() -> str:
    """Generate a variable symbol (VS) - 10 digits."""
    return str(random.randint(1000000000, 9999999999))


def generate_ss() -> str:
    """Generate a specific symbol (SS) - 10 digits."""
    return str(random.randint(1000000000, 9999999999))


def generate_ks() -> str:
    """Generate a constant symbol (KS) - 4 digits."""
    # Common KS values in Czech banking
    common_ks = ["0558", "0308", "1142", "0008", "0300"]
    # Sometimes use common value, sometimes random
    if random.random() > 0.3:
        return random.choice(common_ks)
    return str(random.randint(1000, 9999)).zfill(4)


def generate_amount(
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
    allow_negative: bool = True,
) -> float:
    """Generate a random transaction amount."""
    if min_amount is None:
        min_amount = -10000.0 if allow_negative else 0.0
    if max_amount is None:
        max_amount = 10000.0

    amount = random.uniform(min_amount, max_amount)
    # Round to 2 decimal places
    return round(amount, 2)


def generate_account_name() -> str:
    """Generate a realistic Czech account name."""
    first_name = random.choice(CZECH_FIRST_NAMES)
    last_name = random.choice(CZECH_LAST_NAMES)
    return f"{last_name}, {first_name}"


def generate_transaction(
    index: int,
    base_transaction_id: int,
    base_order_id: int,
    date_from: datetime,
    date_to: datetime,
    account_id: str,
    bank_id: str,
    currency: str,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
) -> Dict[str, Any]:
    """Generate a single transaction."""
    tx_date = generate_timestamp(date_from, date_to)
    tx_type = random.choice(TRANSACTION_TYPES)
    amount = generate_amount(min_amount, max_amount)

    # Determine if transaction has counterpart account based on type
    has_counterpart = tx_type not in ["Připsaný úrok", "Připsaná provize"]

    transaction: Dict[str, Any] = {
        "column22": {"value": generate_transaction_id(base_transaction_id, index), "name": "ID pohybu", "id": 22},
        "column0": {"value": tx_date, "name": "Datum", "id": 0},
        "column1": {"value": amount, "name": "Objem", "id": 1},
        "column14": {"value": currency, "name": "Měna", "id": 14},
        "column8": {"value": tx_type, "name": "Typ", "id": 8},
        "column17": {"value": generate_order_id(base_order_id, index), "name": "ID pokynu", "id": 17},
    }

    # Add counterpart account fields if applicable
    if has_counterpart:
        counterpart_account = generate_account_id()
        counterpart_bank = random.choice(BANK_CODES)
        transaction["column2"] = {"value": counterpart_account, "name": "Protiúčet", "id": 2}
        transaction["column3"] = {"value": counterpart_bank, "name": "Kód banky", "id": 3}
        transaction["column12"] = {
            "value": random.choice(BANK_NAMES),
            "name": "Název banky",
            "id": 12,
        }
        # Add payment symbols (KS, VS, SS)
        transaction["column4"] = {"value": generate_ks(), "name": "KS", "id": 4}
        transaction["column5"] = {"value": generate_vs(), "name": "VS", "id": 5}
        transaction["column6"] = {"value": generate_ss(), "name": "SS", "id": 6}

        # Sometimes add account name
        if random.random() > 0.3:
            transaction["column10"] = {
                "value": generate_account_name(),
                "name": "Názevprotiúčtu",
                "id": 10,
            }

        # Sometimes add user identification
        if random.random() > 0.5:
            transaction["column7"] = {
                "value": random.choice(["", " ", f"Nákup: {generate_account_name()}"]),
                "name": "Uživatelská identifikace",
                "id": 7,
            }

        # Sometimes add performer name
        if random.random() > 0.6:
            transaction["column9"] = {
                "value": generate_account_name(),
                "name": "Proved1",
                "id": 9,
            }

        # Sometimes add comment
        if random.random() > 0.7:
            transaction["column25"] = {
                "value": random.choice(["", "Platba za služby", "Nákup zboží", ""]),
                "name": "Komentář",
                "id": 25,
            }
    else:
        # For interest/provision transactions, set most fields to null
        for col_id in [2, 3, 4, 5, 6, 7, 9, 10, 12, 16, 18, 25, 26]:
            transaction[f"column{col_id}"] = None

    # Set remaining columns to null
    for col_id in [16, 18, 26]:
        if f"column{col_id}" not in transaction:
            transaction[f"column{col_id}"] = None

    return transaction


def generate_statement(
    account_id: Optional[str] = None,
    bank_id: Optional[str] = None,
    currency: str = "CZK",
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    num_transactions: int = 10,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
    opening_balance: Optional[float] = None,
) -> Dict[str, Any]:
    """Generate a complete FIO bank statement JSON structure."""
    # Generate or use provided account details
    if not account_id:
        account_id = generate_account_id()
    if not bank_id:
        bank_id = random.choice(BANK_CODES)

    # Parse dates
    if date_from:
        try:
            date_from_dt = datetime.strptime(date_from, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Invalid date_from format: {date_from}. Use YYYY-MM-DD")
    else:
        date_from_dt = datetime.now() - timedelta(days=30)

    if date_to:
        try:
            date_to_dt = datetime.strptime(date_to, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Invalid date_to format: {date_to}. Use YYYY-MM-DD")
    else:
        date_to_dt = datetime.now()

    if date_from_dt > date_to_dt:
        raise ValueError("date_from must be before date_to")

    # Generate transactions
    base_transaction_id = random.randint(1000000000, 2000000000)
    base_order_id = random.randint(2000000000, 3000000000)
    transactions = []
    closing_balance = opening_balance if opening_balance is not None else 0.0

    for i in range(num_transactions):
        tx = generate_transaction(
            i,
            base_transaction_id,
            base_order_id,
            date_from_dt,
            date_to_dt,
            account_id,
            bank_id,
            currency,
            min_amount,
            max_amount,
        )
        transactions.append(tx)
        closing_balance += tx["column1"]["value"]

    # Sort transactions by date
    transactions.sort(key=lambda x: x["column0"]["value"])

    # Calculate date range from transactions
    if transactions:
        date_start = transactions[0]["column0"]["value"]
        date_end = transactions[-1]["column0"]["value"]
    else:
        date_start = int(date_from_dt.timestamp() * 1000)
        date_end = int(date_to_dt.timestamp() * 1000)

    # Generate IDs - find min and max IDs from transactions
    if transactions:
        transaction_ids = [tx["column22"]["value"] for tx in transactions]
        id_from = min(transaction_ids)
        id_to = max(transaction_ids)
    else:
        id_from = base_transaction_id
        id_to = base_transaction_id
    id_last_download = id_to - random.randint(0, 10)

    statement = {
        "accountStatement": {
            "info": {
                "accountId": account_id,
                "bankId": bank_id,
                "currency": currency,
                "iban": generate_iban(bank_id, account_id),
                "bic": generate_bic(bank_id),
                "openingBalance": round(opening_balance if opening_balance is not None else 0.0, 2),
                "closingBalance": round(closing_balance, 2),
                "dateStart": date_start,
                "dateEnd": date_end,
                "yearList": None,
                "idList": None,
                "idFrom": id_from,
                "idTo": id_to,
                "idLastDownload": id_last_download,
            },
            "transactionList": {"transaction": transactions},
        }
    }

    return statement


def generate_statement_from_params(params: StatementGenerationParams) -> Dict[str, Any]:
    """Generate a statement from a StatementGenerationParams model."""
    return generate_statement(
        account_id=params.account_id,
        bank_id=params.bank_id,
        currency=params.currency,
        date_from=params.date_from,
        date_to=params.date_to,
        num_transactions=params.num_transactions,
        min_amount=params.min_amount,
        max_amount=params.max_amount,
        opening_balance=params.opening_balance,
    )

