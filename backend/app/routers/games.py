from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.attempt import AttemptResponse, GuessRequest, GuessResponse
from app.schemas.game import GameCreateResponse
from app.schemas.ranking import RankingEntryResponse
from app.services.game_service import GameService

router = APIRouter(prefix="/games", tags=["Games"])


@router.get("/ranking/list", response_model=list[RankingEntryResponse])
def get_ranking(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = GameService(db)
    return service.get_ranking()


@router.post("", response_model=GameCreateResponse, status_code=status.HTTP_201_CREATED)
def create_game(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = GameService(db)
    game = service.create_game(current_user)
    return game


@router.get("/{game_code}", response_model=GameCreateResponse)
def get_game(
    game_code: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = GameService(db)
    return service.get_game_by_code(current_user, game_code)


@router.post("/{game_code}/guess", response_model=GuessResponse)
def make_guess(
    game_code: str,
    data: GuessRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = GameService(db)
    return service.make_guess(current_user, game_code, data.guess)


@router.get("/{game_code}/attempts", response_model=list[AttemptResponse])
def list_attempts(
    game_code: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = GameService(db)
    return service.get_attempts(current_user, game_code)
