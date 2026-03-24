from pydantic import BaseModel, ConfigDict


class GameCreateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    code: str
    remaining_attempts: int
    is_finished: bool
    is_won: bool
    final_score: int
    duration_seconds: int
