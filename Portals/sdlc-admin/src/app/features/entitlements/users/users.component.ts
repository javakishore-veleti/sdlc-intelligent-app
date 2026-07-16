import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';

import { BatchPaginator } from '../../../core/utils/batch-paginator';
import { Employee } from '../../../core/models/master-data.models';
import { MasterDataService } from '../../../core/services/master-data.service';

@Component({
  selector: 'app-users',
  standalone: true,
  imports: [CommonModule],
  template: `
    <h2>Users</h2>

    <p *ngIf="pager.error" class="error">{{ pager.error }}</p>

    <table>
      <thead>
        <tr><th>Name</th><th>Email</th><th>Title</th><th>Status</th></tr>
      </thead>
      <tbody>
        <tr *ngFor="let u of pager.pageItems">
          <td>{{ u.first_name }} {{ u.last_name }}</td>
          <td>{{ u.email }}</td>
          <td>{{ u.title || '—' }}</td>
          <td>{{ u.status }}</td>
        </tr>
        <tr *ngIf="!pager.loading && pager.loaded.length === 0">
          <td colspan="4" class="muted">No users found.</td>
        </tr>
      </tbody>
    </table>

    <div class="pager">
      <button (click)="pager.prev()" [disabled]="!pager.canPrev || pager.loading">‹ Prev</button>
      <span class="pageinfo">
        Page {{ pager.currentPage }} of {{ pager.totalClientPages }}
        <span *ngIf="pager.hasMoreServer" class="more">(+more)</span>
      </span>
      <button (click)="pager.next()" [disabled]="!pager.canNext || pager.loading">Next ›</button>
      <span class="loaded muted">{{ pager.loaded.length }} loaded{{ pager.loading ? ' · loading…' : '' }}</span>
    </div>
  `,
  styles: [
    `
      h2 { margin-top: 0; }
      .pager { display: flex; align-items: center; gap: 12px; margin-top: 12px; }
      .pageinfo { font-size: 14px; }
      .more { color: var(--muted); font-size: 12px; }
      .loaded { margin-left: auto; font-size: 12px; }
      .muted { color: var(--muted); }
      .error { color: #b00020; }
    `,
  ],
})
export class UsersComponent implements OnInit {
  // 10 rows per client page; fetch 100 from the server at a time.
  pager = new BatchPaginator<Employee>(
    (skip, limit) => this.api.getEmployees(skip, limit),
    10,
    100,
  );

  constructor(private api: MasterDataService) {}

  ngOnInit(): void {
    this.pager.init();
  }
}
