from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate, UserOut
from app.dependencies import role_required, get_current_user
from app.database import get_db

router = APIRouter()

@router.post("/create", summary="Создать пользователя")
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(role_required(["admin", "manager"]))
):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    if current_user["role"] == "manager":
        if user.role != "user":
            raise HTTPException(status_code=403, detail="Managers can only create users")
    elif current_user["role"] == "admin":
        if user.role not in ["admin", "manager"]:
            raise HTTPException(status_code=403, detail="Invalid role specified")

    manager_id = current_user["id"] if current_user["role"] == "manager" else None

    new_user = User(
        username=user.username,
        hashed_password=user.password + "hased :)",
        role=user.role,
        manager_id=manager_id
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"username": new_user.username, "role": new_user.role, "manager_id": new_user.manager_id}

@router.get("/", response_model=list[UserOut], summary="Получить список пользователей")
def get_users(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] == "admin":
        users = db.query(User).all()
    elif current_user["role"] == "manager":
        users = db.query(User).filter(User.manager_id == current_user["id"]).all()
    else:
        users = db.query(User).filter(User.id == current_user["id"]).all()

    return users
