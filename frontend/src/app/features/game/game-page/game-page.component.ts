import { CommonModule } from '@angular/common';
import { Component, DestroyRef, inject } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { forkJoin } from 'rxjs';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';

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
  private destroyRef = inject(DestroyRef);

  gameCode = '';
  game: GameResponse | null = null;
  attempts: AttemptResponse[] = [];
  boardRows = Array.from({ length: 10 }, (_, index) => 10 - index);
  readonly validColors = ['R', 'G', 'B', 'Y', 'O', 'P'];
  isLoading = true;
  isSubmitting = false;
  errorMessage = '';

  form = this.fb.nonNullable.group({
    guess: ['', [Validators.required, Validators.minLength(4), Validators.maxLength(4)]]
  });

  get latestAttempt(): AttemptResponse | null {
    return this.attempts[0] ?? null;
  }

  get attemptsUsed(): number {
    return this.attempts.length;
  }

  ngOnInit(): void {
    this.route.paramMap
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe((params) => {
        this.gameCode = params.get('code') ?? '';
        this.resetViewState();
        this.loadGameData();
      });
  }

  loadGameData(showLoadingState = true): void {
    if (!this.gameCode) {
      this.errorMessage = 'Codigo do jogo nao encontrado.';
      this.isLoading = false;
      return;
    }

    if (showLoadingState) {
      this.isLoading = true;
    }

    this.errorMessage = '';

    forkJoin({
      game: this.gameService.getGame(this.gameCode),
      attempts: this.gameService.getAttempts(this.gameCode)
    }).subscribe({
      next: ({ game, attempts }) => {
        this.game = game;
        this.attempts = [...attempts].reverse();
        this.isLoading = false;
      },
      error: () => {
        this.errorMessage = 'Nao foi possivel carregar os dados da partida.';
        this.isLoading = false;
      }
    });
  }

  private resetViewState(): void {
    this.game = null;
    this.attempts = [];
    this.errorMessage = '';
    this.isLoading = true;
    this.form.reset();
  }

  submitGuess(): void {
    if (this.form.invalid || !this.gameCode || this.game?.is_finished) {
      this.form.markAllAsTouched();
      return;
    }

    this.errorMessage = '';

    const guess = this.form.controls.guess.getRawValue().trim().toUpperCase();

    if (guess.length !== 4) {
      this.errorMessage = 'Digite exatamente 4 letras.';
      return;
    }

    if ([...guess].some((color) => !this.validColors.includes(color))) {
      this.errorMessage = 'Use apenas R, G, B, Y, O e P.';
      return;
    }

    this.isSubmitting = true;
    this.form.controls.guess.setValue(guess);

    this.gameService.makeGuess(this.gameCode, { guess }).subscribe({
      next: () => {
        this.form.reset();
        this.loadGameData(false);
      },
      error: (error) => {
        this.errorMessage =
          error?.error?.message ??
          error?.error?.detail ??
          'Nao foi possivel enviar o palpite.';
        this.isSubmitting = false;
      },
      complete: () => {
        this.isSubmitting = false;
      }
    });
  }

  getAttemptForRow(rowNumber: number): AttemptResponse | undefined {
    return this.attempts[10 - rowNumber];
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
    this.isSubmitting = true;
    this.errorMessage = '';

    this.gameService.createGame().subscribe({
      next: (game) => {
        this.router.navigate(['/games', game.code]);
      },
      error: () => {
        this.errorMessage = 'Nao foi possivel criar um novo jogo.';
        this.isSubmitting = false;
      },
      complete: () => {
        this.isSubmitting = false;
      }
    });
  }

  goHome(): void {
    this.router.navigate(['/home']);
  }

  logout(): void {
    this.authService.logout();
    this.router.navigate(['/login']);
  }
}
