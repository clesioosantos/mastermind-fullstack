from sqlalchemy.orm import Session

from app.models.game import Game


class GameRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_code(self, game_code: str) -> Game | None:
        return self.db.query(Game).filter(Game.code == game_code).first()

    def get_by_code_and_user(self, game_code: str, user_id: int) -> Game | None:
        return (
            self.db.query(Game)
            .filter(Game.code == game_code, Game.user_id == user_id)
            .first()
        )

    def create(self, game: Game) -> Game:
        self.db.add(game)
        self.db.commit()
        self.db.refresh(game)
        return game

    def update(self, game: Game) -> Game:
        self.db.add(game)
        self.db.commit()
        self.db.refresh(game)
        return game
