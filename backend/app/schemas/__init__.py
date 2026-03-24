from app.schemas.auth import TokenResponse, UserLoginRequest, UserRegisterRequest, UserResponse
from app.schemas.attempt import AttemptResponse, GuessRequest, GuessResponse
from app.schemas.common import ErrorResponse, MessageResponse
from app.schemas.game import GameCreateResponse
from app.schemas.ranking import RankingEntryResponse

__all__ = [
    "ErrorResponse",
    "GameCreateResponse",
    "AttemptResponse",
    "GuessRequest",
    "GuessResponse",
    "MessageResponse",
    "RankingEntryResponse",
    "TokenResponse",
    "UserLoginRequest",
    "UserRegisterRequest",
    "UserResponse",
]
