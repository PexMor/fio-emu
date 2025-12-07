"""Router for emulator control endpoints."""
from typing import Any, Dict, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/emu/v1", tags=["emulator"])

# In-memory storage for injected responses
_injected_periods_data: Optional[Dict[str, Any]] = None


class PeriodsInjectionRequest(BaseModel):
    """Request model for injecting periods response data."""

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

