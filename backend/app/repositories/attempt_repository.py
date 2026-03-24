from sqlalchemy.orm import Session

from app.models.attempt import Attempt


class AttemptRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_by_game_id(self, game_id: int) -> list[Attempt]:
        return (
            self.db.query(Attempt)
            .filter(Attempt.game_id == game_id)
            .order_by(Attempt.id.asc())
            .all()
        )

    def create(self, attempt: Attempt) -> Attempt:
        self.db.add(attempt)
        self.db.commit()
        self.db.refresh(attempt)
        return attempt
