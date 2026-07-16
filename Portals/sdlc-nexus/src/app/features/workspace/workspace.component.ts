import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs';

import { BatchPaginator } from '../../core/utils/batch-paginator';
import { WorkspaceService } from '../../core/services/workspace.service';

interface Column {
  header: string;
  key: string;
}
interface Tab {
  label: string;
  columns: Column[];
  fetch: (skip: number, limit: number) => Observable<any[]>;
}

@Component({
  selector: 'app-workspace',
  standalone: true,
  imports: [CommonModule],
  template: `
    <h1>Workspace</h1>
    <p class="muted">Scoped to your projects (admins see all). Switch user in the top bar.</p>

    <div class="tabs">
      <button
        *ngFor="let t of tabs"
        (click)="select(t)"
        [class.active]="t === active"
        class="tab"
      >
        {{ t.label }}
      </button>
    </div>

    <p *ngIf="pager.error" class="error">{{ pager.error }}</p>

    <table>
      <thead>
        <tr><th *ngFor="let c of active.columns">{{ c.header }}</th></tr>
      </thead>
      <tbody>
        <tr *ngFor="let row of pager.pageItems">
          <td *ngFor="let c of active.columns">{{ cell(row, c.key) }}</td>
        </tr>
        <tr *ngIf="!pager.loading && pager.loaded.length === 0">
          <td [attr.colspan]="active.columns.length" class="muted">Nothing here yet.</td>
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
      h1 { margin-top: 0; margin-bottom: 4px; }
      .muted { color: var(--muted); }
      .error { color: #b00020; }
      .tabs { display: flex; gap: 6px; margin: 16px 0; flex-wrap: wrap; }
      .tab { border-radius: 999px; padding: 6px 14px; }
      .tab.active { background: var(--primary); color: #fff; border-color: var(--primary); }
      .pager { display: flex; align-items: center; gap: 12px; margin-top: 12px; }
      .loaded { margin-left: auto; font-size: 12px; }
      td { font-size: 13px; }
    `,
  ],
})
export class WorkspaceComponent implements OnInit {
  tabs: Tab[];
  active!: Tab;
  pager!: BatchPaginator<any>;

  constructor(private ws: WorkspaceService) {
    this.tabs = [
      {
        label: 'Epics',
        columns: [{ header: 'Title', key: 'title' }, { header: 'Status', key: 'status' }, { header: 'Project', key: 'project_id' }],
        fetch: (s, l) => ws.getEpics(s, l) as Observable<any[]>,
      },
      {
        label: 'Features',
        columns: [{ header: 'Title', key: 'title' }, { header: 'Status', key: 'status' }, { header: 'Epic', key: 'epic_id' }],
        fetch: (s, l) => ws.getFeatures(s, l) as Observable<any[]>,
      },
      {
        label: 'Sprints',
        columns: [{ header: 'Name', key: 'name' }, { header: 'Status', key: 'status' }, { header: 'Start', key: 'start_date' }, { header: 'End', key: 'end_date' }],
        fetch: (s, l) => ws.getSprints(s, l) as Observable<any[]>,
      },
      {
        label: 'Releases',
        columns: [{ header: 'Name', key: 'name' }, { header: 'Status', key: 'status' }, { header: 'Release date', key: 'release_date' }],
        fetch: (s, l) => ws.getReleases(s, l) as Observable<any[]>,
      },
      {
        label: 'Stories',
        columns: [{ header: 'Title', key: 'title' }, { header: 'Status', key: 'status' }, { header: 'Points', key: 'story_points' }],
        fetch: (s, l) => ws.getStories(s, l) as Observable<any[]>,
      },
    ];
  }

  ngOnInit(): void {
    this.select(this.tabs[0]);
  }

  select(tab: Tab): void {
    this.active = tab;
    this.pager = new BatchPaginator<any>((s, l) => tab.fetch(s, l), 10, 100);
    this.pager.init();
  }

  cell(row: any, key: string): string {
    const v = row[key];
    return v === null || v === undefined || v === '' ? '—' : String(v);
  }
}
