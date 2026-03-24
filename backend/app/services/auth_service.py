from sqlalchemy.orm import Session

from app.core.exceptions import ConflictException, UnauthorizedException
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import UserLoginRequest, UserRegisterRequest


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)

    def register(self, payload: UserRegisterRequest):
        existing_user = self.user_repository.get_by_email(payload.email)
        if existing_user:
            raise ConflictException("Email already registered")

        user = User(
            email=payload.email,
            full_name=payload.full_name,
            hashed_password=hash_password(payload.password),
            is_active=True,
        )

        return self.user_repository.create(user)

    def login(self, payload: UserLoginRequest):
        user = self.user_repository.get_by_email(payload.email)

        if not user or not verify_password(payload.password, user.hashed_password):
            raise UnauthorizedException("Invalid credentials")

        token = create_access_token(subject=str(user.id))

        return {
            "access_token": token,
            "token_type": "bearer",
            "user": user,
        }
