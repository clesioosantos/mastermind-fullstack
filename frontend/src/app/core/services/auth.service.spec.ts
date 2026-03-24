import { TestBed } from '@angular/core/testing';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { provideHttpClient } from '@angular/common/http';

import { environment } from '../../../environments/environment';
import { AuthService } from './auth.service';

describe('AuthService', () => {
  let service: AuthService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    localStorage.clear();

    TestBed.configureTestingModule({
      providers: [
        AuthService,
        provideHttpClient(),
        provideHttpClientTesting(),
      ],
    });

    service = TestBed.inject(AuthService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
    localStorage.clear();
  });

  it('stores token and user after login', () => {
    service.login({ email: 'player@example.com', password: 'secret123' }).subscribe();

    const request = httpMock.expectOne(`${environment.apiUrl}/auth/login`);
    expect(request.request.method).toBe('POST');

    request.flush({
      access_token: 'jwt-token',
      token_type: 'bearer',
      user: {
        id: 1,
        email: 'player@example.com',
        full_name: 'Player One',
        is_active: true,
      },
    });

    expect(localStorage.getItem('access_token')).toBe('jwt-token');
    expect(service.getUser()?.email).toBe('player@example.com');
    expect(service.isAuthenticated()).toBeTrue();
  });
});
