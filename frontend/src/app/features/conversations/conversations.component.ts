import { Component } from '@angular/core';

@Component({
  selector: 'app-conversations',
  standalone: true,
  template: `
    <div class="p-6">
      <h1 class="text-2xl font-bold mb-4">Conversations</h1>
      <p class="text-gray-600">Manage customer conversations</p>
    </div>
  `,
})
export class ConversationsComponent {}
