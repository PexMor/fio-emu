"""Router for by-id endpoint - official statements."""
from fastapi import APIRouter

router = APIRouter(prefix="/v1/rest/by-id", tags=["by-id"])


@router.get("/{token}/{year}/{id}/transactions.{format}")
async def get_statement_by_id(
    token: str,
    year: int,
    id: int,
    format: str,
):
    """
    Get official statement by year and ID.

    Format can be: xml, json, csv, ofx, gpc, html, sta, cbaxml, sbaxml, pdf
    """
    # TODO: Implement route handler
    return {"message": "Not implemented yet"}

