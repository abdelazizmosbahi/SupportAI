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
  selector: 'app-register',
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
          <mat-card-title class="text-2xl font-bold">Register</mat-card-title>
          <mat-card-subtitle>Create your SupportAI account</mat-card-subtitle>
        </mat-card-header>
        <mat-card-content class="mt-4">
          <form (ngSubmit)="onSubmit()" #registerForm="ngForm">
            <div class="flex gap-3">
              <mat-form-field appearance="outline" class="w-full">
                <mat-label>First Name</mat-label>
                <input matInput [(ngModel)]="firstName" name="firstName" placeholder="First name">
              </mat-form-field>
              <mat-form-field appearance="outline" class="w-full">
                <mat-label>Last Name</mat-label>
                <input matInput [(ngModel)]="lastName" name="lastName" placeholder="Last name">
              </mat-form-field>
            </div>
            <mat-form-field appearance="outline" class="w-full">
              <mat-label>Email</mat-label>
              <input matInput type="email" [(ngModel)]="email" name="email" required email placeholder="Enter your email">
            </mat-form-field>
            <mat-form-field appearance="outline" class="w-full">
              <mat-label>Password</mat-label>
              <input matInput type="password" [(ngModel)]="password" name="password" required minlength="8" placeholder="Enter your password">
              <mat-hint>At least 8 characters with uppercase, lowercase, and a number</mat-hint>
            </mat-form-field>
            @if (errorMessage) {
              <mat-error class="mb-2">
                {{ errorMessage }}
              </mat-error>
            }
            <button mat-raised-button color="primary" class="w-full" type="submit" [disabled]="loading || registerForm.invalid">
              @if (loading) {
                <mat-spinner diameter="20" class="inline-block mr-2"></mat-spinner>
              } @else {
                <span>Register</span>
              }
            </button>
          </form>
        </mat-card-content>
        <mat-card-actions>
          <a mat-button routerLink="/login" class="w-full text-center">Already have an account? Login</a>
        </mat-card-actions>
      </mat-card>
    </div>
  `,
})
export class RegisterComponent {
  private authService = inject(AuthService);
  private router = inject(Router);

  firstName = '';
  lastName = '';
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
    this.authService
      .register({
        email: this.email,
        password: this.password,
        first_name: this.firstName || undefined,
        last_name: this.lastName || undefined,
      })
      .subscribe({
        next: () => {
          this.loading = false;
          this.router.navigate(['/login']);
        },
        error: (err) => {
          this.loading = false;
          this.errorMessage = err?.error?.detail ?? 'Registration failed. Please try again.';
        },
      });
  }
}
