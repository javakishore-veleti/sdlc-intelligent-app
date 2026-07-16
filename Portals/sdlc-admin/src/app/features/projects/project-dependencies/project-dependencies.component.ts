import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';

import { BatchPaginator } from '../../../core/utils/batch-paginator';
import { ProjectDependency } from '../../../core/models/master-data.models';
import { MasterDataService } from '../../../core/services/master-data.service';

@Component({
  selector: 'app-project-dependencies',
  standalone: true,
  imports: [CommonModule],
  template: `
    <h2>Project Dependencies</h2>
    <p *ngIf="pager.error" class="error">{{ pager.error }}</p>

    <table>
      <thead>
        <tr><th>Project</th><th>Depends On Project</th><th>Capability</th><th>Description</th></tr>
      </thead>
      <tbody>
        <tr *ngFor="let d of pager.pageItems">
          <td>{{ d.project_id }}</td>
          <td>{{ d.depends_on_project_id }}</td>
          <td>{{ d.depends_on_capability_id || '—' }}</td>
          <td>{{ d.description || '—' }}</td>
        </tr>
        <tr *ngIf="!pager.loading && pager.loaded.length === 0">
          <td colspan="4" class="muted">No dependencies found.</td>
        </tr>
      </tbody>
    </table>

    <div class="pager">
      <button (click)="pager.prev()" [disabled]="!pager.canPrev || pager.loading">‹ Prev</button>
      <span>Page {{ pager.currentPage }} of {{ pager.totalClientPages }}</span>
      <button (click)="pager.next()" [disabled]="!pager.canNext || pager.loading">Next ›</button>
      <span class="loaded muted">{{ pager.loaded.length }} loaded{{ pager.loading ? ' · loading…' : '' }}</span>
    </div>
  `,
  styles: [
    `
      h2 { margin-top: 0; }
      .pager { display: flex; align-items: center; gap: 12px; margin-top: 12px; }
      .loaded { margin-left: auto; font-size: 12px; }
      .muted { color: var(--muted); }
      .error { color: #b00020; }
      td { font-size: 13px; }
    `,
  ],
})
export class ProjectDependenciesComponent implements OnInit {
  pager = new BatchPaginator<ProjectDependency>(
    (skip, limit) => this.api.getProjectDependencies(skip, limit),
    10,
    100,
  );

  constructor(private api: MasterDataService) {}

  ngOnInit(): void {
    this.pager.init();
  }
}
