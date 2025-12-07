"""Router for periods endpoint - movements for a specific period."""
import copy
from datetime import datetime
from typing import Any, Dict, Optional

from fastapi import APIRouter, HTTPException

from fioemu.routers.emu import get_injected_periods_data

router = APIRouter(prefix="/v1/rest/periods", tags=["periods"])


def parse_date(date_str: str) -> int:
    """
    Parse date string to timestamp in milliseconds.

    Supports formats: YYYY-MM-DD, DD.MM.YYYY, or timestamp in milliseconds
    """
    try:
        # Try parsing as timestamp (milliseconds)
        return int(date_str)
    except ValueError:
        pass

    # Try parsing as date string
    for fmt in ["%Y-%m-%d", "%d.%m.%Y"]:
        try:
            dt = datetime.strptime(date_str, fmt)
            return int(dt.timestamp() * 1000)
        except ValueError:
            continue

    raise HTTPException(
        status_code=400,
        detail=f"Invalid date format: {date_str}. Use YYYY-MM-DD, DD.MM.YYYY, or timestamp",
    )


def filter_transactions_by_date(
    transactions: list[Dict[str, Any]], date_from: int, date_to: int
) -> list[Dict[str, Any]]:
    """Filter transactions by date range."""
    filtered = []
    for transaction in transactions:
        column0 = transaction.get("column0")
        if column0 and column0.get("value"):
            tx_date = column0["value"]
            if date_from <= tx_date <= date_to:
                filtered.append(transaction)
    return filtered


@router.get("/{token}/{date_from}/{date_to}/transactions.{format}")
async def get_period_transactions(
    token: str,
    date_from: str,
    date_to: str,
    format: str,
):
    """
    Get movements on account for a specific period.

    Format can be: xml, json, csv, ofx, gpc, html, sta, cbaxml, sbaxml
    Currently only JSON format is implemented.
    """
    if format != "json":
        raise HTTPException(
            status_code=501, detail=f"Format {format} is not yet implemented"
        )

    # Get injected data
    injected_data = get_injected_periods_data()
    if not injected_data:
        raise HTTPException(
            status_code=404,
            detail="No data available. Please inject data via POST /emu/v1/periods",
        )

    # Parse dates
    try:
        date_from_ms = parse_date(date_from)
        date_to_ms = parse_date(date_to)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid date format: {e}")

    # Deep copy the injected data to avoid mutating the original
    response_data = copy.deepcopy(injected_data)

    # Filter transactions by date range
    transactions = response_data["accountStatement"]["transactionList"]["transaction"]
    filtered_transactions = filter_transactions_by_date(
        transactions, date_from_ms, date_to_ms
    )

    # Update response with filtered transactions
    response_data["accountStatement"]["transactionList"][
        "transaction"
    ] = filtered_transactions

    # Update info section dates if needed
    info = response_data["accountStatement"]["info"]
    if filtered_transactions:
        # Update dateStart and dateEnd based on filtered transactions
        dates = [
            tx["column0"]["value"]
            for tx in filtered_transactions
            if tx.get("column0") and tx["column0"].get("value")
        ]
        if dates:
            info["dateStart"] = min(dates)
            info["dateEnd"] = max(dates)

    return response_data

