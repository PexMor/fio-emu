"""Router for last endpoint - movements since last download."""
from fastapi import APIRouter

router = APIRouter(prefix="/v1/rest/last", tags=["last"])


@router.get("/{token}/transactions.{format}")
async def get_last_transactions(
    token: str,
    format: str,
):
    """
    Get movements on account since last download.

    Format can be: xml, json, csv, ofx, gpc, html, sta, cbaxml, sbaxml
    """
    # TODO: Implement route handler
    return {"message": "Not implemented yet"}

