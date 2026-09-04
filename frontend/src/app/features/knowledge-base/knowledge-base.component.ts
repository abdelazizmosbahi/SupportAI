import { Component } from '@angular/core';

@Component({
  selector: 'app-knowledge-base',
  standalone: true,
  template: `
    <div class="p-6">
      <h1 class="text-2xl font-bold mb-4">Knowledge Base</h1>
      <p class="text-gray-600">Manage documents and knowledge base</p>
    </div>
  `,
})
export class KnowledgeBaseComponent {}
