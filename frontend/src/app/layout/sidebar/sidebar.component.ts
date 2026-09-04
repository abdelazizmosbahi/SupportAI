import { Component } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { MatIconModule } from '@angular/material/icon';
import { MatListModule } from '@angular/material/list';

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [RouterLink, RouterLinkActive, MatIconModule, MatListModule],
  template: `
    <div class="sidebar">
      <div class="sidebar-brand">
        <mat-icon>support_agent</mat-icon>
        <span>SupportAI</span>
      </div>
      <mat-nav-list>
        <a mat-list-item routerLink="/dashboard" routerLinkActive="active-link">
          <mat-icon matListItemIcon>dashboard</mat-icon>
          <span matListItemTitle>Dashboard</span>
        </a>
        <a mat-list-item routerLink="/conversations" routerLinkActive="active-link">
          <mat-icon matListItemIcon>chat</mat-icon>
          <span matListItemTitle>Conversations</span>
        </a>
        <a mat-list-item routerLink="/knowledge-base" routerLinkActive="active-link">
          <mat-icon matListItemIcon>library_books</mat-icon>
          <span matListItemTitle>Knowledge Base</span>
        </a>
        <a mat-list-item routerLink="/tickets" routerLinkActive="active-link">
          <mat-icon matListItemIcon>confirmation_number</mat-icon>
          <span matListItemTitle>Tickets</span>
        </a>
        <a mat-list-item routerLink="/evaluations" routerLinkActive="active-link">
          <mat-icon matListItemIcon>assessment</mat-icon>
          <span matListItemTitle>Evaluations</span>
        </a>
        <a mat-list-item routerLink="/analytics" routerLinkActive="active-link">
          <mat-icon matListItemIcon>analytics</mat-icon>
          <span matListItemTitle>Analytics</span>
        </a>
        <a mat-list-item routerLink="/settings" routerLinkActive="active-link">
          <mat-icon matListItemIcon>settings</mat-icon>
          <span matListItemTitle>Settings</span>
        </a>
      </mat-nav-list>
    </div>
  `,
  styles: [`
    .sidebar {
      width: 250px;
      height: 100%;
      background: #1a1a2e;
      color: white;
      display: flex;
      flex-direction: column;
    }
    .sidebar-brand {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 16px;
      font-size: 18px;
      font-weight: 500;
      border-bottom: 1px solid rgba(255,255,255,0.1);
    }
    mat-nav-list {
      flex: 1;
      padding-top: 8px;
    }
    a {
      color: rgba(255,255,255,0.7);
      margin: 2px 8px;
      border-radius: 8px;
    }
    a:hover {
      background: rgba(255,255,255,0.1);
      color: white;
    }
    .active-link {
      background: rgba(103, 58, 183, 0.3) !important;
      color: white !important;
    }
  `]
})
export class SidebarComponent {}
