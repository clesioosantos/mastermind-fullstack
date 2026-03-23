import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { Router } from '@angular/router';

import { User } from '../../core/models/auth.models';
import { AuthService } from '../../core/services/auth.service';
import { GameService } from '../../core/services/game.service';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent {
  private authService = inject(AuthService);
  private gameService = inject(GameService);
  private router = inject(Router);

  user: User | null = this.authService.getUser();
  isLoading = false;
  errorMessage = '';

  createGame(): void {
    this.isLoading = true;
    this.errorMessage = '';

    this.gameService.createGame().subscribe({
      next: (game) => {
        this.router.navigate(['/games', game.code]);
      },
      error: () => {
        this.errorMessage = 'Não foi possível criar um novo jogo.';
        this.isLoading = false;
      },
      complete: () => {
        this.isLoading = false;
      }
    });
  }

  logout(): void {
    this.authService.logout();
    this.router.navigate(['/login']);
  }
}
