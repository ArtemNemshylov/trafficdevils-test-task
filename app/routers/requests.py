from http.client import HTTPException

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models import Request, User
from app.schemas import RequestCreate, RequestOut
from app.database import get_db
from app.dependencies import get_current_user
from app.functions import send_to_telegram

router = APIRouter()

@router.post("/", response_model=RequestOut, summary="Прием и обработка JSON-запросов")
def handle_request(
    request: RequestCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    telegram_response = send_to_telegram(
        bottoken=request.bottoken,
        chatid=request.chatid,
        message=request.message
    )

    new_request = Request(
        bottoken=request.bottoken,
        chatid=request.chatid,
        message=request.message,
        response=str(telegram_response),
        user_id=current_user["id"]
    )
    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    if not telegram_response.get("ok", True):
        raise HTTPException()

    return new_request

@router.get("/", response_model=list[RequestOut], summary="Получить список запросов")
def get_all_requests(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] == "admin":
        return db.query(Request).all()
    elif current_user["role"] == "manager":
        return db.query(Request).join(User).filter(User.manager_id == current_user["id"]).all()
    else:
        return db.query(Request).filter(Request.user_id == current_user["id"]).all()
