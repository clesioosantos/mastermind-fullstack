import random
import string

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.attempt import Attempt
from app.models.game import Game
from app.models.user import User


class GameService:
    COLORS = ["R", "G", "B", "Y", "O", "P"]

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

    @staticmethod
    def create_game(db: Session, user: User):
        code = GameService.generate_game_code()
        while db.query(Game).filter(Game.code == code).first():
            code = GameService.generate_game_code()

        game = Game(
            code=code,
            user_id=user.id,
            secret_code=GameService.generate_secret_code(),
            remaining_attempts=10,
            is_finished=False,
            is_won=False,
        )

        db.add(game)
        db.commit()
        db.refresh(game)

        return game

    @staticmethod
    def get_game_by_code(db: Session, user: User, game_code: str) -> Game:
        game = (
            db.query(Game)
            .filter(Game.code == game_code, Game.user_id == user.id)
            .first()
        )

        if not game:
            raise HTTPException(status_code=404, detail="Game not found")

        return game

    @staticmethod
    def get_attempts(db: Session, user: User, game_code: str):
        game = GameService.get_game_by_code(db, user, game_code)

        attempts = (
            db.query(Attempt)
            .filter(Attempt.game_id == game.id)
            .order_by(Attempt.id.asc())
            .all()
        )

        return attempts

    @staticmethod
    def make_guess(db: Session, user: User, game_code: str, guess: str):
        game = GameService.get_game_by_code(db, user, game_code)

        if game.is_finished:
            raise HTTPException(status_code=400, detail="Game already finished")

        if game.remaining_attempts <= 0:
            raise HTTPException(status_code=400, detail="No attempts left")

        if len(guess) != 4:
            raise HTTPException(status_code=400, detail="Guess must be 4 characters")

        if any(color not in GameService.COLORS for color in guess):
            raise HTTPException(status_code=400, detail="Invalid colors")

        correct = GameService.calculate_correct(game.secret_code, guess)

        game.remaining_attempts -= 1

        attempt = Attempt(
            game_id=game.id,
            guess=guess,
            correct_count=correct,
        )

        db.add(attempt)

        if correct == 4:
            game.is_finished = True
            game.is_won = True
        elif game.remaining_attempts == 0:
            game.is_finished = True
            game.is_won = False

        db.commit()
        db.refresh(game)

        return {
            "correct_count": correct,
            "remaining_attempts": game.remaining_attempts,
            "is_finished": game.is_finished,
            "is_won": game.is_won,
        }
