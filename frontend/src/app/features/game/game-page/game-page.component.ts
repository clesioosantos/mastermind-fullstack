import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { forkJoin } from 'rxjs';

import { AttemptResponse, GameResponse } from '../../../core/models/game.models';
import { AuthService } from '../../../core/services/auth.service';
import { GameService } from '../../../core/services/game.service';

@Component({
  selector: 'app-game-page',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  templateUrl: './game-page.component.html',
  styleUrl: './game-page.component.css'
})
export class GamePageComponent {
  private route = inject(ActivatedRoute);
  private router = inject(Router);
  private fb = inject(FormBuilder);
  private gameService = inject(GameService);
  private authService = inject(AuthService);

  gameCode = this.route.snapshot.paramMap.get('code') ?? '';
  game: GameResponse | null = null;
  attempts: AttemptResponse[] = [];
  boardRows = Array.from({ length: 10 }, (_, index) => 10 - index);
  isLoading = true;
  isSubmitting = false;
  errorMessage = '';

  form = this.fb.nonNullable.group({
    guess: ['', [Validators.required, Validators.minLength(4), Validators.maxLength(4)]]
  });

  ngOnInit(): void {
    this.loadGameData();
  }

  loadGameData(): void {
    if (!this.gameCode) {
      this.errorMessage = 'Codigo do jogo nao encontrado.';
      this.isLoading = false;
      return;
    }

    this.isLoading = true;
    this.errorMessage = '';

    forkJoin({
      game: this.gameService.getGame(this.gameCode),
      attempts: this.gameService.getAttempts(this.gameCode)
    }).subscribe({
      next: ({ game, attempts }) => {
        this.game = game;
        this.attempts = attempts;
        this.isLoading = false;
      },
      error: () => {
        this.errorMessage = 'Nao foi possivel carregar os dados da partida.';
        this.isLoading = false;
      }
    });
  }

  submitGuess(): void {
    if (this.form.invalid || !this.gameCode || this.game?.is_finished) {
      this.form.markAllAsTouched();
      return;
    }

    this.isSubmitting = true;
    this.errorMessage = '';

    const guess = this.form.controls.guess.getRawValue().toUpperCase();

    this.gameService.makeGuess(this.gameCode, { guess }).subscribe({
      next: (response) => {
        this.game = {
          code: this.gameCode,
          remaining_attempts: response.remaining_attempts,
          is_finished: response.is_finished,
          is_won: response.is_won
        };
        this.form.reset();
        this.loadAttemptsOnly();
      },
      error: (error) => {
        this.errorMessage = error?.error?.detail ?? 'Nao foi possivel enviar o palpite.';
        this.isSubmitting = false;
      },
      complete: () => {
        this.isSubmitting = false;
      }
    });
  }

  private loadAttemptsOnly(): void {
    this.gameService.getAttempts(this.gameCode).subscribe({
      next: (attempts) => {
        this.attempts = attempts;
      }
    });
  }

  getAttemptForRow(rowNumber: number): AttemptResponse | undefined {
    return this.attempts[rowNumber - 1];
  }

  getGuessSlots(guess: string | undefined): string[] {
    const normalizedGuess = guess ?? '';
    return Array.from({ length: 4 }, (_, index) => normalizedGuess[index] ?? '');
  }

  getFeedbackSlots(correctCount: number | undefined): boolean[] {
    const count = correctCount ?? 0;
    return Array.from({ length: 4 }, (_, index) => index < count);
  }

  getPegClass(color: string): string {
    const palette: Record<string, string> = {
      R: 'peg-red',
      G: 'peg-green',
      B: 'peg-blue',
      Y: 'peg-yellow',
      O: 'peg-orange',
      P: 'peg-purple'
    };

    return palette[color] ?? 'peg-empty';
  }

  newGame(): void {
    this.router.navigate(['/home']);
  }

  logout(): void {
    this.authService.logout();
    this.router.navigate(['/login']);
  }
}
