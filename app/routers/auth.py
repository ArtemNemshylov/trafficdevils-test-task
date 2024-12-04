from fastapi import APIRouter, Depends, HTTPException, Form
from app.dependencies import create_access_token
from app.database import get_db
from app.models import User
from sqlalchemy.orm import Session
router = APIRouter()

@router.post("/token", summary="Получить JWT-токен")
def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == username).first()
    if not user or user.hashed_password != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role, "id": user.id}
    )
    return {"access_token": access_token, "token_type": "bearer"}
