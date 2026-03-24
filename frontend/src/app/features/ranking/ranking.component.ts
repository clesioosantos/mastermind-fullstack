import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { Router } from '@angular/router';

import { RankingEntryResponse } from '../../core/models/game.models';
import { AuthService } from '../../core/services/auth.service';
import { GameService } from '../../core/services/game.service';

@Component({
  selector: 'app-ranking',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './ranking.component.html',
  styleUrl: './ranking.component.css'
})
export class RankingComponent {
  private router = inject(Router);
  private authService = inject(AuthService);
  private gameService = inject(GameService);

  ranking: RankingEntryResponse[] = [];
  isLoading = true;
  errorMessage = '';

  ngOnInit(): void {
    this.loadRanking();
  }

  loadRanking(): void {
    this.isLoading = true;
    this.errorMessage = '';

    this.gameService.getRanking().subscribe({
      next: (ranking) => {
        this.ranking = ranking;
        this.isLoading = false;
      },
      error: () => {
        this.errorMessage = 'Nao foi possivel carregar o ranking.';
        this.isLoading = false;
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
