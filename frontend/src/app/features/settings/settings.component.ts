import { Component } from '@angular/core';

@Component({
  selector: 'app-settings',
  standalone: true,
  template: `
    <div class="p-6">
      <h1 class="text-2xl font-bold mb-4">Settings</h1>
      <p class="text-gray-600">Organization and account settings</p>
    </div>
  `,
})
export class SettingsComponent {}
