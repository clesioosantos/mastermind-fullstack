from sqlalchemy.orm import Session

from app.core.exceptions import ConflictException, UnauthorizedException
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.schemas.auth import UserLoginRequest, UserRegisterRequest


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def register(self, payload: UserRegisterRequest):
        existing_user = self.db.query(User).filter(User.email == payload.email).first()
        if existing_user:
            raise ConflictException("Email already registered")

        user = User(
            email=payload.email,
            full_name=payload.full_name,
            hashed_password=hash_password(payload.password),
            is_active=True,
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def login(self, payload: UserLoginRequest):
        user = self.db.query(User).filter(User.email == payload.email).first()

        if not user or not verify_password(payload.password, user.hashed_password):
            raise UnauthorizedException("Invalid credentials")

        token = create_access_token(subject=str(user.id))

        return {
            "access_token": token,
            "token_type": "bearer",
            "user": user,
        }
