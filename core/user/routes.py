# user.py
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, Response, Request
from sqlalchemy.orm import Session
from datetime import timedelta

from core.src.db import get_db
from . import models, schemas
from core.auth import jwt_auth, utils, schemas as auth_schemas
from core.src.config import settings

router = APIRouter(tags=['User'], prefix='/user')

# ------------------------------- REGISTER -----------------------------
@router.post("/register")
async def register(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.UserModel).filter(models.UserModel.email == user_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    hashed_password = utils.get_password_hash(user_data.password)
    user = models.UserModel(
        **user_data.model_dump(exclude={"password"}),
        password_hash=hashed_password
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "User registered successfully", "user": {"id": user.id, "email": user.email}}


# ------------------------------- LOGIN --------------------------------
@router.post("/login", response_model=auth_schemas.Token)
async def login(credentials: auth_schemas.UserLogin, response: Response, db: Session = Depends(get_db)):
    user = db.query(models.UserModel).filter(models.UserModel.email == credentials.email).first()
    if not user or not utils.verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate Access/Refresh Token
    access_token = jwt_auth.create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = jwt_auth.create_refresh_token(data={"sub": str(user.id)})

    # Set Cookies
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        secure=True,  # فقط در HTTPS
        samesite="strict",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600
    )

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


# ------------------ REFRESH TOKEN -----------------
@router.post("/refresh", response_model=auth_schemas.Token)
async def refresh_token_endpoint(request: Request, response: Response, db: Session = Depends(get_db)):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token not found")

    try:
        payload = jwt_auth.decode_token(refresh_token, "refresh")
        user_id: str = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    except HTTPException:
        raise

    # check if user is in the db
    user = db.query(models.UserModel).filter(models.UserModel.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    # generate new token
    new_access_token = jwt_auth.create_access_token(data={"sub": str(user.id)})
    new_refresh_token = jwt_auth.create_refresh_token(data={"sub": str(user.id)})  # rotate refresh token

    # update cookie
    response.set_cookie(
        key="access_token",
        value=f"Bearer {new_access_token}",
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600
    )

    return {"access_token": new_access_token, "refresh_token": new_refresh_token, "token_type": "bearer"}


# --------------------- GET CURRENT USER ---------------------
@router.get("/current")
async def get_current_user(current_user: models.UserModel = Depends(jwt_auth.get_current_user_from_cookie)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "is_active": current_user.is_active,
    }


# ----------------------- LOGOUT -----------------------------
@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token", secure=True, httponly=True, samesite="strict")
    response.delete_cookie("refresh_token", secure=True, httponly=True, samesite="strict")
    return {"message": "Logged out successfully"}


# ------------------- FORGET PASSWORD  -----------------------
@router.post("/forget-password")
async def forget_password(email: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    user = db.query(models.UserModel).filter(models.UserModel.email == email).first()
    if not user:
        return {"message": "If email exists, a reset link has been sent."}

    reset_token = jwt_auth.create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=60)
    )
    # we can add a method for sending email
    return {"reset_token": reset_token}