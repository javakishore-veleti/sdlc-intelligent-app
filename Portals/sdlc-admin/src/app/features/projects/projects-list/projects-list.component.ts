import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';

import { BatchPaginator } from '../../../core/utils/batch-paginator';
import { Project } from '../../../core/models/master-data.models';
import { MasterDataService } from '../../../core/services/master-data.service';

@Component({
  selector: 'app-projects-list',
  standalone: true,
  imports: [CommonModule],
  template: `
    <h2>Projects</h2>
    <p *ngIf="pager.error" class="error">{{ pager.error }}</p>

    <table>
      <thead>
        <tr><th>Name</th><th>Code</th><th>Status</th><th>Description</th></tr>
      </thead>
      <tbody>
        <tr *ngFor="let p of pager.pageItems">
          <td>{{ p.name }}</td>
          <td>{{ p.code || '—' }}</td>
          <td>{{ p.status }}</td>
          <td>{{ p.description || '—' }}</td>
        </tr>
        <tr *ngIf="!pager.loading && pager.loaded.length === 0">
          <td colspan="4" class="muted">No projects found.</td>
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
    `,
  ],
})
export class ProjectsListComponent implements OnInit {
  pager = new BatchPaginator<Project>((skip, limit) => this.api.getProjects(skip, limit), 10, 100);

  constructor(private api: MasterDataService) {}

  ngOnInit(): void {
    this.pager.init();
  }
}
