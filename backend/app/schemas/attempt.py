from pydantic import BaseModel, ConfigDict


class GuessRequest(BaseModel):
    guess: str


class GuessResponse(BaseModel):
    correct_count: int
    remaining_attempts: int
    is_finished: bool
    is_won: bool


class AttemptResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    guess: str
    correct_count: int
