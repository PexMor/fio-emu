"""Router for emulator control endpoints."""
from typing import Any, Dict, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from fioemu.generator import StatementGenerationParams, generate_statement_from_params

router = APIRouter(prefix="/emu/v1", tags=["emulator"])

# In-memory storage for injected responses
_injected_periods_data: Optional[Dict[str, Any]] = None


class PeriodsInjectionRequest(BaseModel):
    """Request model for injecting periods response data."""

    accountStatement: Dict[str, Any]


class GenerateResponse(BaseModel):
    """Response model for the generate endpoint."""

    status: str
    message: str
    accountStatement: Dict[str, Any]


@router.post("/periods")
async def inject_periods_response(data: PeriodsInjectionRequest) -> Dict[str, str]:
    """
    Inject JSON response data for periods endpoint.

    This endpoint allows you to inject a complete JSON response that will be
    returned by the /v1/rest/periods/{token}/{date_from}/{date_to}/transactions.json
    endpoint, filtered by date_from and date_to.
    """
    global _injected_periods_data
    _injected_periods_data = data.model_dump()
    return {"status": "success", "message": "Periods response data injected"}


@router.delete("/periods")
async def clear_periods_response() -> Dict[str, str]:
    """Clear injected periods response data."""
    global _injected_periods_data
    _injected_periods_data = None
    return {"status": "success", "message": "Periods response data cleared"}


def get_injected_periods_data() -> Optional[Dict[str, Any]]:
    """Get the currently injected periods data."""
    return _injected_periods_data


@router.post("/generate", response_model=GenerateResponse)
async def generate_and_inject_statement(
    params: StatementGenerationParams,
) -> GenerateResponse:
    """
    Generate random FIO bank statement data and inject it for the periods endpoint.

    This endpoint combines the functionality of `fiocli` CLI tool with automatic
    injection into the emulator. The generated statement will be returned and
    also set as the response for the periods endpoint.

    Parameters are the same as the `fiocli` CLI command:
    - account_id: Account ID (10 digits, default: random)
    - bank_id: Bank code (default: random from common Czech banks)
    - currency: Currency code (default: CZK)
    - date_from: Start date in YYYY-MM-DD format (default: 30 days ago)
    - date_to: End date in YYYY-MM-DD format (default: today)
    - num_transactions: Number of transactions to generate (default: 10)
    - min_amount: Minimum transaction amount (default: -10000)
    - max_amount: Maximum transaction amount (default: 10000)
    - opening_balance: Opening balance (default: 0.0)

    Returns the generated statement data and injects it for the periods endpoint.
    """
    global _injected_periods_data

    try:
        statement = generate_statement_from_params(params)
        _injected_periods_data = statement
        return GenerateResponse(
            status="success",
            message="Statement generated and injected for periods endpoint",
            accountStatement=statement["accountStatement"],
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
