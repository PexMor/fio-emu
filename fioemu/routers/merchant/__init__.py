"""Router for merchant endpoint - card transactions."""
from fastapi import APIRouter

router = APIRouter(prefix="/v1/rest/merchant", tags=["merchant"])


@router.get("/{token}/{date_from}/{date_to}/transactions.{format}")
async def get_merchant_transactions(
    token: str,
    date_from: str,
    date_to: str,
    format: str,
):
    """
    Get card transactions from POS terminals or payment gateway for a period.

    Format can be: xml, csv
    """
    # TODO: Implement route handler
    return {"message": "Not implemented yet"}

