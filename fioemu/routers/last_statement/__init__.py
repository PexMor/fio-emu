"""Router for lastStatement endpoint - get last statement number."""
from fastapi import APIRouter

router = APIRouter(prefix="/v1/rest/lastStatement", tags=["last-statement"])


@router.get("/{token}/statement")
async def get_last_statement(
    token: str,
):
    """
    Get the number of the last created official statement.
    """
    # TODO: Implement route handler
    return {"message": "Not implemented yet"}

