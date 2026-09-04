import { HttpErrorResponse, HttpEvent, HttpHandlerFn, HttpInterceptorFn, HttpRequest } from '@angular/common/http';
import { inject } from '@angular/core';
import { BehaviorSubject, Observable, switchMap, throwError } from 'rxjs';
import { catchError, filter, take } from 'rxjs/operators';

import { AuthService } from '../auth/auth.service';

const REFRESH_URL = '/api/v1/auth/refresh';
let isRefreshing = false;
const refreshSubject$ = new BehaviorSubject<string | null>(null);

function isAuthEndpoint(url: string): boolean {
  return url.includes('/api/v1/auth/login') || url.includes('/api/v1/auth/register');
}

function isWhitelisted(url: string): boolean {
  return url.includes(REFRESH_URL) || isAuthEndpoint(url);
}

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const authService = inject(AuthService);

  if (isWhitelisted(req.url)) {
    return next(req);
  }

  const accessToken = authService.getAccessToken();
  let authReq: HttpRequest<unknown> = req;

  if (accessToken) {
    authReq = req.clone({
      setHeaders: { Authorization: `Bearer ${accessToken}` },
    });
  }

  return next(authReq).pipe(
    catchError((error: HttpErrorResponse) => {
      if (error.status === 401 && accessToken && !req.url.includes(REFRESH_URL)) {
        return handle401(authReq, next, authService);
      }
      return throwError(() => error);
    }),
  );
};

function handle401(req: HttpRequest<unknown>, next: HttpHandlerFn, authService: AuthService): Observable<HttpEvent<unknown>> {
  if (isRefreshing) {
    return refreshSubject$.pipe(
      filter(token => token !== null),
      take(1),
      switchMap(token => {
        return next(
          req.clone({ setHeaders: { Authorization: `Bearer ${token}` } }),
        );
      }),
    );
  }

  isRefreshing = true;
  refreshSubject$.next(null);

  return authService.refreshToken().pipe(
    switchMap((token: string) => {
      isRefreshing = false;
      refreshSubject$.next(token);
      return next(req.clone({ setHeaders: { Authorization: `Bearer ${token}` } }));
    }),
    catchError((err) => {
      isRefreshing = false;
      authService.clearSession();
      return throwError(() => err);
    }),
  );
}
