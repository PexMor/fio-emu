"""Router for set-last-id endpoint - set last downloaded movement ID."""
from fastapi import APIRouter

router = APIRouter(prefix="/v1/rest/set-last-id", tags=["set-last-id"])


@router.get("/{token}/{id}/")
async def set_last_id(
    token: str,
    id: int,
):
    """
    Set the ID of the last successfully downloaded movement.
    """
    # TODO: Implement route handler
    return {"message": "Not implemented yet"}

