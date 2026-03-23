from sqlalchemy.orm import declarative_base

Base = declarative_base()

from app.models.user import User  # noqa: E402,F401
from app.models.game import Game  # noqa: E402,F401
from app.models.attempt import Attempt  # noqa: E402,F401
