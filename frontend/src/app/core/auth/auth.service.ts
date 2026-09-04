import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, of, throwError } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';
import { Router } from '@angular/router';

import { LoginResponse, MessageResponse, RegisterRequest, TokenResponse, User } from '../models/auth';

const ACCESS_TOKEN_KEY = 'access_token';
const REFRESH_TOKEN_KEY = 'refresh_token';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private http = inject(HttpClient);
  private router = inject(Router);

  private currentUserSubject = new BehaviorSubject<User | null>(this.getStoredUser());
  currentUser$ = this.currentUserSubject.asObservable();

  private isRefreshing = false;

  getAccessToken(): string | null {
    return localStorage.getItem(ACCESS_TOKEN_KEY);
  }

  getRefreshToken(): string | null {
    return localStorage.getItem(REFRESH_TOKEN_KEY);
  }

  private getStoredUser(): User | null {
    const raw = localStorage.getItem('user');
    return raw ? (JSON.parse(raw) as User) : null;
  }

  isAuthenticated(): boolean {
    return !!this.getAccessToken();
  }

  get currentUser(): User | null {
    return this.currentUserSubject.value;
  }

  login(email: string, password: string): Observable<User> {
    return this.http.post<LoginResponse>('/api/v1/auth/login', { email, password }).pipe(
      tap(response => this.setSession(response)),
      map(response => response.user),
    );
  }

  register(data: RegisterRequest): Observable<User> {
    return this.http.post<User>('/api/v1/auth/register', data);
  }

  logout(): Observable<void> {
    const accessToken = this.getAccessToken();
    if (!accessToken) {
      this.clearSession();
      return of(undefined);
    }
    return this.http.post<MessageResponse>('/api/v1/auth/logout', {}).pipe(
      catchError(() => of({} as MessageResponse)),
      tap(() => this.clearSession()),
      map(() => undefined),
    );
  }

  getCurrentUser(): Observable<User> {
    return this.http.get<User>('/api/v1/auth/me').pipe(
      tap(user => this.setStoredUser(user)),
    );
  }

  refreshToken(): Observable<string> {
    const refreshToken = this.getRefreshToken();
    if (!refreshToken) {
      return throwError(() => new Error('No refresh token available'));
    }
    return this.http
      .post<TokenResponse>('/api/v1/auth/refresh', { refresh_token: refreshToken })
      .pipe(
        tap(response => this.setSession(response)),
        map(response => response.access_token),
      );
  }

  handleUnauthorized(): Observable<string> {
    if (this.isRefreshing) {
      return throwError(() => new Error('Refresh already in progress'));
    }
    this.isRefreshing = true;
    return this.refreshToken().pipe(
      tap({
        next: () => {
          this.isRefreshing = false;
        },
        error: () => {
          this.isRefreshing = false;
          this.clearSession();
          this.router.navigate(['/login']);
        },
      }),
    );
  }

  private setSession(response: LoginResponse | TokenResponse): void {
    localStorage.setItem(ACCESS_TOKEN_KEY, response.access_token);
    localStorage.setItem(REFRESH_TOKEN_KEY, response.refresh_token);
    this.setStoredUser(response.user);
  }

  private setStoredUser(user: User): void {
    localStorage.setItem('user', JSON.stringify(user));
    this.currentUserSubject.next(user);
  }

  clearSession(): void {
    localStorage.removeItem(ACCESS_TOKEN_KEY);
    localStorage.removeItem(REFRESH_TOKEN_KEY);
    localStorage.removeItem('user');
    this.currentUserSubject.next(null);
  }
}
