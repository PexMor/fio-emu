"""Router for set-last-date endpoint - set last failed download date."""
from fastapi import APIRouter

router = APIRouter(prefix="/v1/rest/set-last-date", tags=["set-last-date"])


@router.get("/{token}/{date}/")
async def set_last_date(
    token: str,
    date: str,
):
    """
    Set the date of the last unsuccessfully downloaded statement.
    """
    # TODO: Implement route handler
    return {"message": "Not implemented yet"}

