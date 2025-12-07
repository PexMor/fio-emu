"""Router for import endpoint - upload payment orders."""
from fastapi import APIRouter, File, Form, UploadFile

router = APIRouter(prefix="/v1/rest/import", tags=["import"])


@router.post("/")
async def import_payment_orders(
    token: str = Form(...),
    type: str = Form(...),  # abo, xml, pain001xml, pain008xml
    file: UploadFile = File(...),
    lang: str = Form(default="CS"),  # CS, sk, en
):
    """
    Import payment orders into the bank.

    Types: abo, xml, pain001xml, pain008xml
    """
    # TODO: Implement route handler
    return {"message": "Not implemented yet"}

