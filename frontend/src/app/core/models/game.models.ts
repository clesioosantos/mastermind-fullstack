export interface GameResponse {
  code: string;
  remaining_attempts: number;
  is_finished: boolean;
  is_won: boolean;
  final_score: number;
  duration_seconds: number;
}

export interface GuessRequest {
  guess: string;
}

export interface GuessResponse {
  correct_count: number;
  remaining_attempts: number;
  is_finished: boolean;
  is_won: boolean;
}

export interface AttemptResponse {
  guess: string;
  correct_count: number;
}

export interface RankingEntryResponse {
  user_id: number;
  full_name: string;
  email: string;
  games_played: number;
  wins: number;
  best_score: number;
}
