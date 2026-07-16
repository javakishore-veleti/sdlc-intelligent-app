import { Component } from '@angular/core';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-projects',
  standalone: true,
  imports: [RouterOutlet, RouterLink, RouterLinkActive],
  template: `
    <div class="layout">
      <aside class="sidenav">
        <div class="sidenav-title">Projects</div>
        <a routerLink="list" routerLinkActive="active">Projects</a>
        <a routerLink="dependencies" routerLinkActive="active">Project Dependencies</a>
        <a routerLink="tech-stack" routerLinkActive="active">Project Tech Stack</a>
      </aside>
      <section class="panel">
        <router-outlet></router-outlet>
      </section>
    </div>
  `,
  styles: [
    `
      .layout { display: grid; grid-template-columns: 200px 1fr; gap: 20px; align-items: start; }
      .sidenav { background: var(--panel); border: 1px solid var(--border); border-radius: 10px; padding: 8px; }
      .sidenav-title { color: var(--muted); font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; padding: 8px 12px; }
      .sidenav a { display: block; padding: 8px 12px; border-radius: 6px; color: var(--text); font-size: 14px; }
      .sidenav a.active { background: var(--primary-weak); color: var(--primary); font-weight: 600; }
      .sidenav a:hover { background: var(--primary-weak); }
      @media (max-width: 720px) { .layout { grid-template-columns: 1fr; } }
    `,
  ],
})
export class ProjectsComponent {}
