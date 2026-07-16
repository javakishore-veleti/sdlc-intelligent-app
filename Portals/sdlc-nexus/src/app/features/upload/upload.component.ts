import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { IngestService } from '../../core/services/ingest.service';
import { IngestLog, IngestResponse } from '../../core/models/models';

@Component({
  selector: 'app-upload',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <h1>Upload Sprint Document</h1>
    <p class="muted">Uploads a PDF to the datalake and triggers ingestion into the vector DB.</p>

    <div class="form">
      <label>PDF file
        <input type="file" accept="application/pdf" (change)="onFile($event)" />
      </label>
      <label>Project ID
        <input type="text" [(ngModel)]="projectId" placeholder="UUID of the project" />
      </label>
      <label>Sprint
        <input type="text" [(ngModel)]="sprint" placeholder="e.g. Sprint 9" />
      </label>
      <label>Uploaded by
        <input type="text" [(ngModel)]="uploadedBy" placeholder="your user / employee id" />
      </label>
      <button (click)="submit()" [disabled]="!file || !projectId || busy">
        {{ busy ? 'Uploading…' : 'Upload & ingest' }}
      </button>
    </div>

    <p *ngIf="error" class="error">{{ error }}</p>

    <div *ngIf="result as r" class="result">
      <strong>Uploaded.</strong>
      Log <code>{{ r.ingest_log.id }}</code> — status {{ r.ingest_log.ingest_process_status }};
      Airflow triggered: {{ r.airflow.triggered }}<span *ngIf="r.airflow.detail"> ({{ r.airflow.detail }})</span>
    </div>

    <h2>Recent ingests</h2>
    <p *ngIf="logsError" class="error">{{ logsError }}</p>
    <table>
      <thead>
        <tr><th>File</th><th>Sprint</th><th>Type</th><th>Storage</th><th>Status</th></tr>
      </thead>
      <tbody>
        <tr *ngFor="let l of logs">
          <td>{{ l.file_name }}</td>
          <td>{{ l.project_sprint || '—' }}</td>
          <td>{{ l.ingest_type }}</td>
          <td>{{ l.storage_type }}</td>
          <td>{{ l.ingest_process_status }}</td>
        </tr>
        <tr *ngIf="logs.length === 0"><td colspan="5" class="muted">No ingests yet.</td></tr>
      </tbody>
    </table>
  `,
  styles: [
    `
      h1 { margin-top: 0; margin-bottom: 4px; }
      h2 { margin-top: 28px; }
      .muted { color: var(--muted); }
      .error { color: #b00020; }
      .form { display: grid; gap: 12px; max-width: 460px; background: var(--panel);
        border: 1px solid var(--border); border-radius: 10px; padding: 20px; }
      .form label { display: grid; gap: 4px; font-size: 13px; color: var(--muted); }
      .form input[type='text'] { font: inherit; padding: 7px 9px; border: 1px solid var(--border); border-radius: 6px; }
      .form button { justify-self: start; background: var(--primary); color: #fff; border-color: var(--primary); padding: 8px 16px; }
      .result { margin: 16px 0; padding: 12px 14px; background: #eef7ee; border: 1px solid #cfe6cf; border-radius: 8px; font-size: 14px; }
      code { background: #eef1f6; padding: 1px 5px; border-radius: 4px; }
    `,
  ],
})
export class UploadComponent implements OnInit {
  file: File | null = null;
  projectId = '';
  sprint = '';
  uploadedBy = '';
  busy = false;
  error = '';
  result?: IngestResponse;

  logs: IngestLog[] = [];
  logsError = '';

  constructor(private ingest: IngestService) {}

  ngOnInit(): void {
    this.loadLogs();
  }

  onFile(event: Event): void {
    const input = event.target as HTMLInputElement;
    this.file = input.files && input.files.length ? input.files[0] : null;
  }

  submit(): void {
    if (!this.file || !this.projectId) return;
    this.busy = true;
    this.error = '';
    this.result = undefined;
    this.ingest.uploadPdf(this.file, this.projectId, this.sprint, this.uploadedBy).subscribe({
      next: (r) => {
        this.result = r;
        this.busy = false;
        this.loadLogs();
      },
      error: (e) => {
        this.error = e?.error?.detail || 'Upload failed. Is Ingest-Extract-Service running?';
        this.busy = false;
      },
    });
  }

  private loadLogs(): void {
    this.ingest.listIngestLogs(0, 20).subscribe({
      next: (l) => (this.logs = l),
      error: () => (this.logsError = 'Could not load ingest history.'),
    });
  }
}
