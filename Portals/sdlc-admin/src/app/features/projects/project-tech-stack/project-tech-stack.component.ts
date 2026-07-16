import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';

import { BatchPaginator } from '../../../core/utils/batch-paginator';
import { ProjectTechStack } from '../../../core/models/master-data.models';
import { MasterDataService } from '../../../core/services/master-data.service';

@Component({
  selector: 'app-project-tech-stack',
  standalone: true,
  imports: [CommonModule],
  template: `
    <h2>Project Tech Stack</h2>
    <p *ngIf="pager.error" class="error">{{ pager.error }}</p>

    <table>
      <thead>
        <tr><th>Project</th><th>Name</th><th>Category</th><th>Version</th></tr>
      </thead>
      <tbody>
        <tr *ngFor="let t of pager.pageItems">
          <td>{{ t.project_id }}</td>
          <td>{{ t.name }}</td>
          <td>{{ t.category }}</td>
          <td>{{ t.version || '—' }}</td>
        </tr>
        <tr *ngIf="!pager.loading && pager.loaded.length === 0">
          <td colspan="4" class="muted">No tech stack entries found.</td>
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
export class ProjectTechStackComponent implements OnInit {
  pager = new BatchPaginator<ProjectTechStack>(
    (skip, limit) => this.api.getProjectTechStacks(skip, limit),
    10,
    100,
  );

  constructor(private api: MasterDataService) {}

  ngOnInit(): void {
    this.pager.init();
  }
}
