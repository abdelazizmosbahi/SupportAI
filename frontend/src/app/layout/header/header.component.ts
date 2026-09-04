import { Component, inject } from '@angular/core';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatMenuModule } from '@angular/material/menu';
import { Router } from '@angular/router';

import { AuthService } from '../../core/auth/auth.service';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [MatToolbarModule, MatIconModule, MatButtonModule, MatMenuModule],
  template: `
    <mat-toolbar class="header">
      <span class="spacer"></span>
      <button mat-icon-button>
        <mat-icon>notifications</mat-icon>
      </button>
      <button mat-icon-button [matMenuTriggerFor]="userMenu">
        <mat-icon>account_circle</mat-icon>
      </button>
      <mat-menu #userMenu="matMenu">
        <span class="px-4 py-2 block text-sm text-gray-600">
          {{ currentUserEmail }}
        </span>
        <button mat-menu-item (click)="onLogout()">
          <mat-icon>logout</mat-icon>
          <span>Logout</span>
        </button>
      </mat-menu>
    </mat-toolbar>
  `,
  styles: [`
    .header {
      background: white;
      color: #333;
      border-bottom: 1px solid #e0e0e0;
      justify-content: flex-end;
    }
    .spacer {
      flex: 1;
    }
  `]
})
export class HeaderComponent {
  private authService = inject(AuthService);
  private router = inject(Router);

  get currentUserEmail(): string {
    return this.authService.currentUser?.email ?? '';
  }

  onLogout(): void {
    this.authService.logout().subscribe(() => {
      this.router.navigate(['/login']);
    });
  }
}
