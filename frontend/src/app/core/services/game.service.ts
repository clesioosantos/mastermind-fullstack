import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { environment } from '../../../environments/environment';
import { AttemptResponse, GameResponse, GuessRequest, GuessResponse, RankingEntryResponse } from '../models/game.models';

@Injectable({
  providedIn: 'root'
})
export class GameService {
  private http = inject(HttpClient);
  private apiUrl = `${environment.apiUrl}/games`;

  createGame(): Observable<GameResponse> {
    return this.http.post<GameResponse>(this.apiUrl, {});
  }

  getGame(code: string): Observable<GameResponse> {
    return this.http.get<GameResponse>(`${this.apiUrl}/${code}`);
  }

  makeGuess(code: string, payload: GuessRequest): Observable<GuessResponse> {
    return this.http.post<GuessResponse>(`${this.apiUrl}/${code}/guess`, payload);
  }

  getAttempts(code: string): Observable<AttemptResponse[]> {
    return this.http.get<AttemptResponse[]>(`${this.apiUrl}/${code}/attempts`);
  }

  getRanking(): Observable<RankingEntryResponse[]> {
    return this.http.get<RankingEntryResponse[]>(`${this.apiUrl}/ranking/list`);
  }
}
