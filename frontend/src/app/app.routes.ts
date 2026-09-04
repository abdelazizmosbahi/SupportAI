import { Routes } from '@angular/router';

export const routes: Routes = [
  { path: '', redirectTo: '/dashboard', pathMatch: 'full' },
  {
    path: 'dashboard',
    loadComponent: () =>
      import('./features/dashboard/dashboard.component').then(m => m.DashboardComponent),
  },
  {
    path: 'conversations',
    loadComponent: () =>
      import('./features/conversations/conversations.component').then(m => m.ConversationsComponent),
  },
  {
    path: 'knowledge-base',
    loadComponent: () =>
      import('./features/knowledge-base/knowledge-base.component').then(m => m.KnowledgeBaseComponent),
  },
  {
    path: 'tickets',
    loadComponent: () =>
      import('./features/tickets/tickets.component').then(m => m.TicketsComponent),
  },
  {
    path: 'evaluations',
    loadComponent: () =>
      import('./features/evaluations/evaluations.component').then(m => m.EvaluationsComponent),
  },
  {
    path: 'analytics',
    loadComponent: () =>
      import('./features/analytics/analytics.component').then(m => m.AnalyticsComponent),
  },
  {
    path: 'settings',
    loadComponent: () =>
      import('./features/settings/settings.component').then(m => m.SettingsComponent),
  },
  {
    path: 'login',
    loadComponent: () =>
      import('./features/auth/login/login.component').then(m => m.LoginComponent),
  },
  {
    path: 'register',
    loadComponent: () =>
      import('./features/auth/register/register.component').then(m => m.RegisterComponent),
  },
];
