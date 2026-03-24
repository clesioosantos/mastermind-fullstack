import random
import string
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.core.exceptions import BadRequestException, NotFoundException
from app.models.attempt import Attempt
from app.models.game import Game
from app.models.user import User
from app.repositories.attempt_repository import AttemptRepository
from app.repositories.game_repository import GameRepository
from app.repositories.user_repository import UserRepository
from app.schemas.ranking import RankingEntryResponse


class GameService:
    COLORS = ["R", "G", "B", "Y", "O", "P"]

    def __init__(self, db: Session):
        self.db = db
        self.game_repository = GameRepository(db)
        self.attempt_repository = AttemptRepository(db)
        self.user_repository = UserRepository(db)

    @staticmethod
    def generate_secret_code():
        return "".join(random.choices(GameService.COLORS, k=4))

    @staticmethod
    def generate_game_code(length=8):
        chars = string.ascii_uppercase + string.digits
        return "".join(random.choices(chars, k=length))

    @staticmethod
    def calculate_correct(secret: str, guess: str) -> int:
        return sum(1 for s, g in zip(secret, guess) if s == g)

    def create_game(self, user: User):
        code = self.generate_game_code()
        while self.game_repository.get_by_code(code):
            code = self.generate_game_code()

        game = Game(
            code=code,
            user_id=user.id,
            secret_code=self.generate_secret_code(),
            remaining_attempts=10,
            is_finished=False,
            is_won=False,
        )

        return self.game_repository.create(game)

    def get_game_by_code(self, user: User, game_code: str) -> Game:
        game = self.game_repository.get_by_code_and_user(game_code, user.id)

        if not game:
            raise NotFoundException("Game not found")

        return game

    def get_attempts(self, user: User, game_code: str):
        game = self.get_game_by_code(user, game_code)
        return self.attempt_repository.list_by_game_id(game.id)

    def make_guess(self, user: User, game_code: str, guess: str):
        game = self.get_game_by_code(user, game_code)

        if game.is_finished:
            raise BadRequestException("Game already finished")

        if game.remaining_attempts <= 0:
            raise BadRequestException("No attempts left")

        if len(guess) != 4:
            raise BadRequestException("Guess must be 4 characters")

        if any(color not in GameService.COLORS for color in guess):
            raise BadRequestException("Invalid colors")

        correct = self.calculate_correct(game.secret_code, guess)

        game.remaining_attempts -= 1

        attempt = Attempt(
            game_id=game.id,
            guess=guess,
            correct_count=correct,
        )

        self.db.add(attempt)

        if correct == 4:
            game.is_finished = True
            game.is_won = True
        elif game.remaining_attempts == 0:
            game.is_finished = True
            game.is_won = False

        if game.is_finished:
            finished_at = datetime.now(timezone.utc)
            game.finished_at = finished_at
            started_at = game.created_at
            if started_at.tzinfo is None:
                started_at = started_at.replace(tzinfo=timezone.utc)

            game.duration_seconds = max(int((finished_at - started_at).total_seconds()), 0)
            game.final_score = self._calculate_score(game, correct)
            self._update_user_best_score(user, game.final_score)

        self.db.commit()
        self.db.refresh(game)

        return {
            "correct_count": correct,
            "remaining_attempts": game.remaining_attempts,
            "is_finished": game.is_finished,
            "is_won": game.is_won,
        }

    def get_ranking(self) -> list[RankingEntryResponse]:
        ranking_rows = self.user_repository.get_ranking()
        return [
            RankingEntryResponse(
                user_id=user.id,
                full_name=user.full_name,
                email=user.email,
                games_played=games_played,
                wins=wins,
                best_score=best_score,
            )
            for user, games_played, wins, best_score in ranking_rows
        ]

    def _update_user_best_score(self, user: User, final_score: int) -> None:
        if final_score > user.best_score:
            user.best_score = final_score
            self.db.add(user)

    @staticmethod
    def _calculate_score(game: Game, correct: int) -> int:
        attempts_used = 10 - game.remaining_attempts
        if game.is_won:
            return 100 + (game.remaining_attempts * 10) + correct - attempts_used
        return max(correct * 5, 0)
