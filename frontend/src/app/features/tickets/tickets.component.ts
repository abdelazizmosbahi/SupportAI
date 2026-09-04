import { Component } from '@angular/core';

@Component({
  selector: 'app-tickets',
  standalone: true,
  template: `
    <div class="p-6">
      <h1 class="text-2xl font-bold mb-4">Tickets</h1>
      <p class="text-gray-600">Manage support tickets</p>
    </div>
  `,
})
export class TicketsComponent {}
