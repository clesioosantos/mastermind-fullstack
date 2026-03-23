export interface GameResponse {
  code: string;
  remaining_attempts: number;
  is_finished: boolean;
  is_won: boolean;
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
