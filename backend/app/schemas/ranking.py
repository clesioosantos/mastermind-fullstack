from pydantic import BaseModel, ConfigDict, EmailStr


class RankingEntryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    full_name: str
    email: EmailStr
    games_played: int
    wins: int
    best_score: int
