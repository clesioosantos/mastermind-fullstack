import { ComponentFixture, TestBed } from '@angular/core/testing';
import { of } from 'rxjs';

import { AuthService } from '../../core/services/auth.service';
import { GameService } from '../../core/services/game.service';
import { RankingComponent } from './ranking.component';

describe('RankingComponent', () => {
  let component: RankingComponent;
  let fixture: ComponentFixture<RankingComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RankingComponent],
      providers: [
        {
          provide: GameService,
          useValue: {
            getRanking: () => of([
              {
                user_id: 1,
                full_name: 'Player One',
                email: 'player@example.com',
                games_played: 3,
                wins: 2,
                best_score: 120,
              },
            ]),
          },
        },
        {
          provide: AuthService,
          useValue: {
            logout: jasmine.createSpy('logout'),
          },
        },
      ],
    }).compileComponents();

    fixture = TestBed.createComponent(RankingComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('loads ranking entries on init', () => {
    expect(component.ranking.length).toBe(1);
    expect(component.ranking[0].full_name).toBe('Player One');
  });
});
