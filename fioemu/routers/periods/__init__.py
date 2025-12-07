"""Router for periods endpoint - movements for a specific period."""
from fastapi import APIRouter

router = APIRouter(prefix="/v1/rest/periods", tags=["periods"])


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
    """
    # TODO: Implement route handler
    return {"message": "Not implemented yet"}

