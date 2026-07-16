import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';

import { MasterDataService } from '../../core/services/master-data.service';
import { DashboardStats } from '../../core/models/master-data.models';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule],
  template: `
    <h1>Dashboard</h1>

    <p *ngIf="loading" class="muted">Loading…</p>
    <p *ngIf="error" class="error">{{ error }}</p>

    <div *ngIf="stats as s" class="grid">
      <section class="tile">
        <div class="tile-label">Projects</div>
        <div class="tile-value">{{ s.project_count }}</div>
      </section>

      <section class="tile wide">
        <div class="tile-label">Top 10 Tech Stacks (by project count)</div>
        <table *ngIf="s.top_tech_stacks.length; else noStacks">
          <thead>
            <tr><th>#</th><th>Tech Stack</th><th>Projects</th></tr>
          </thead>
          <tbody>
            <tr *ngFor="let t of s.top_tech_stacks; let i = index">
              <td>{{ i + 1 }}</td>
              <td>{{ t.name }}</td>
              <td>{{ t.project_count }}</td>
            </tr>
          </tbody>
        </table>
        <ng-template #noStacks><p class="muted">No tech stacks yet.</p></ng-template>
      </section>
    </div>

    <p *ngIf="stats as s" class="footnote">
      Cached at {{ s.generated_at }} · TTL {{ s.cache_ttl_seconds / 3600 | number: '1.0-1' }}h
    </p>
  `,
  styles: [
    `
      h1 { margin-top: 0; }
      .grid { display: grid; grid-template-columns: 240px 1fr; gap: 16px; align-items: start; }
      .tile { background: var(--panel); border: 1px solid var(--border); border-radius: 10px; padding: 20px; }
      .tile-label { color: var(--muted); font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.03em; }
      .tile-value { font-size: 48px; font-weight: 700; margin-top: 8px; color: var(--primary); }
      .wide { padding: 0; overflow: hidden; }
      .wide .tile-label { padding: 20px 20px 0; }
      .wide table { margin-top: 12px; }
      .muted { color: var(--muted); }
      .error { color: #b00020; }
      .footnote { color: var(--muted); font-size: 12px; margin-top: 16px; }
      @media (max-width: 720px) { .grid { grid-template-columns: 1fr; } }
    `,
  ],
})
export class DashboardComponent implements OnInit {
  stats?: DashboardStats;
  loading = true;
  error = '';

  constructor(private api: MasterDataService) {}

  ngOnInit(): void {
    this.api.getDashboardStats().subscribe({
      next: (s) => {
        this.stats = s;
        this.loading = false;
      },
      error: () => {
        this.error = 'Failed to load dashboard. Is Master-Data-Service running?';
        this.loading = false;
      },
    });
  }
}
