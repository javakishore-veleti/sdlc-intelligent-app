import { Component } from '@angular/core';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, RouterLink, RouterLinkActive],
  template: `
    <header class="topbar">
      <div class="brand">SDLC Admin</div>
      <nav class="menu">
        <a routerLink="/dashboard" routerLinkActive="active">Dashboard</a>
        <a routerLink="/entitlements" routerLinkActive="active">Entitlements</a>
        <a routerLink="/projects" routerLinkActive="active">Projects</a>
      </nav>
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
        gap: 32px;
        background: var(--primary);
        color: #fff;
        padding: 0 24px;
        height: 56px;
      }
      .brand { font-weight: 700; font-size: 16px; letter-spacing: 0.02em; }
      .menu { display: flex; gap: 8px; height: 100%; }
      .menu a {
        display: flex;
        align-items: center;
        padding: 0 16px;
        height: 100%;
        color: #dfe7f5;
        border-bottom: 3px solid transparent;
      }
      .menu a.active { color: #fff; border-bottom-color: #fff; font-weight: 600; }
      .menu a:hover { color: #fff; }
      .content { padding: 24px; max-width: 1200px; margin: 0 auto; }
    `,
  ],
})
export class AppComponent {}
