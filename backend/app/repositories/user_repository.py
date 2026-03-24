from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from app.models.game import Game
from app.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def create(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_ranking(self) -> list[tuple[User, int, int, int]]:
        return (
            self.db.query(
                User,
                func.count(Game.id).label("games_played"),
                func.coalesce(func.sum(Game.is_won), 0).label("wins"),
                func.coalesce(func.max(Game.final_score), 0).label("best_score"),
            )
            .outerjoin(Game, Game.user_id == User.id)
            .group_by(User.id)
            .order_by(desc("best_score"), desc("wins"), User.full_name.asc())
            .all()
        )
