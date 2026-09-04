import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [FormsModule, RouterLink, MatCardModule, MatInputModule, MatButtonModule, MatIconModule],
  template: `
    <div class="flex items-center justify-center min-h-screen bg-gray-100">
      <mat-card class="w-full max-w-md p-8">
        <mat-card-header>
          <mat-card-title class="text-2xl font-bold">Register</mat-card-title>
          <mat-card-subtitle>Create your SupportAI account</mat-card-subtitle>
        </mat-card-header>
        <mat-card-content class="mt-4">
          <mat-form-field appearance="outline" class="w-full">
            <mat-label>First Name</mat-label>
            <input matInput [(ngModel)]="firstName" placeholder="Enter your first name">
          </mat-form-field>
          <mat-form-field appearance="outline" class="w-full">
            <mat-label>Last Name</mat-label>
            <input matInput [(ngModel)]="lastName" placeholder="Enter your last name">
          </mat-form-field>
          <mat-form-field appearance="outline" class="w-full">
            <mat-label>Email</mat-label>
            <input matInput type="email" [(ngModel)]="email" placeholder="Enter your email">
          </mat-form-field>
          <mat-form-field appearance="outline" class="w-full">
            <mat-label>Password</mat-label>
            <input matInput type="password" [(ngModel)]="password" placeholder="Enter your password">
          </mat-form-field>
        </mat-card-content>
        <mat-card-actions class="flex flex-col gap-2">
          <button mat-raised-button color="primary" class="w-full">Register</button>
          <a mat-button routerLink="/login" class="text-center">Already have an account? Login</a>
        </mat-card-actions>
      </mat-card>
    </div>
  `,
})
export class RegisterComponent {
  firstName = '';
  lastName = '';
  email = '';
  password = '';
}
