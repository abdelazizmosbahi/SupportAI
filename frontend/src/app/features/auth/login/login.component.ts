import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';

import { AuthService } from '../../../core/auth/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    FormsModule,
    RouterLink,
    MatCardModule,
    MatInputModule,
    MatButtonModule,
    MatIconModule,
    MatProgressSpinnerModule,
  ],
  template: `
    <div class="flex items-center justify-center min-h-screen bg-gray-100">
      <mat-card class="w-full max-w-md p-8">
        <mat-card-header>
          <mat-card-title class="text-2xl font-bold">Login</mat-card-title>
          <mat-card-subtitle>Sign in to SupportAI</mat-card-subtitle>
        </mat-card-header>
        <mat-card-content class="mt-4">
          <form (ngSubmit)="onSubmit()" #loginForm="ngForm">
            <mat-form-field appearance="outline" class="w-full">
              <mat-label>Email</mat-label>
              <input matInput type="email" [(ngModel)]="email" name="email" required email placeholder="Enter your email">
            </mat-form-field>
            <mat-form-field appearance="outline" class="w-full">
              <mat-label>Password</mat-label>
              <input matInput type="password" [(ngModel)]="password" name="password" required placeholder="Enter your password">
            </mat-form-field>
            @if (errorMessage) {
              <mat-error class="mb-2">
                {{ errorMessage }}
              </mat-error>
            }
            <button mat-raised-button color="primary" class="w-full" type="submit" [disabled]="loading || loginForm.invalid">
              @if (loading) {
                <mat-spinner diameter="20" class="inline-block mr-2"></mat-spinner>
              } @else {
                <span>Login</span>
              }
            </button>
          </form>
        </mat-card-content>
        <mat-card-actions>
          <a mat-button routerLink="/register" class="w-full text-center">Don't have an account? Register</a>
        </mat-card-actions>
      </mat-card>
    </div>
  `,
})
export class LoginComponent {
  private authService = inject(AuthService);
  private router = inject(Router);

  email = '';
  password = '';
  loading = false;
  errorMessage = '';

  onSubmit(): void {
    if (this.loading) {
      return;
    }
    this.loading = true;
    this.errorMessage = '';
    this.authService.login(this.email, this.password).subscribe({
      next: () => {
        this.loading = false;
        this.router.navigate(['/dashboard']);
      },
      error: (err) => {
        this.loading = false;
        this.errorMessage = err?.error?.detail ?? 'Login failed. Please try again.';
      },
    });
  }
}
