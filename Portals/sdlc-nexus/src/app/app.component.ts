import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';

import { UserContextService } from './core/services/user-context.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterOutlet, RouterLink, RouterLinkActive],
  template: `
    <header class="topbar">
      <div class="brand">SDLC Nexus</div>
      <nav class="menu">
        <a routerLink="/workspace" routerLinkActive="active">Workspace</a>
        <a routerLink="/upload" routerLinkActive="active">Upload</a>
        <a routerLink="/assistant" routerLinkActive="active">Assistant</a>
      </nav>
      <div class="user">
        <span class="user-label">Signed in as</span>
        <input
          [ngModel]="user.email"
          (ngModelChange)="user.setEmail($event)"
          list="user-presets"
          class="user-input"
          title="Stand-in for login: sets X-User-Email (admin@example.com sees all projects)"
        />
        <datalist id="user-presets">
          <option value="demo@example.com"></option>
          <option value="user@example.com"></option>
          <option value="admin@example.com"></option>
        </datalist>
      </div>
    </header>
    <main class="content">
      <router-outlet></router-outlet>
    </main>
  `,
  styles: [
    `
      .topbar {
        display: flex;
        align-items: center;
        gap: 24px;
        background: var(--primary);
        color: #fff;
        padding: 0 24px;
        height: 56px;
      }
      .brand { font-weight: 700; font-size: 16px; }
      .menu { display: flex; gap: 8px; height: 100%; }
      .menu a {
        display: flex; align-items: center; padding: 0 16px; height: 100%;
        color: #dfe7f5; border-bottom: 3px solid transparent;
      }
      .menu a.active { color: #fff; border-bottom-color: #fff; font-weight: 600; }
      .menu a:hover { color: #fff; }
      .user { margin-left: auto; display: flex; align-items: center; gap: 8px; font-size: 13px; }
      .user-label { color: #cdd9ef; }
      .user-input {
        font: inherit; font-size: 13px; padding: 5px 8px; border-radius: 6px;
        border: 1px solid rgba(255, 255, 255, 0.4); background: rgba(255, 255, 255, 0.12);
        color: #fff; width: 200px;
      }
      .content { padding: 24px; max-width: 1100px; margin: 0 auto; }
    `,
  ],
})
export class AppComponent {
  constructor(public user: UserContextService) {}
}
