import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { environment } from '../../../environments/environment';
import { IngestLog, IngestResponse } from '../models/models';

@Injectable({ providedIn: 'root' })
export class IngestService {
  private readonly base = environment.ingestApiBaseUrl;

  constructor(private http: HttpClient) {}

  uploadPdf(
    file: File,
    projectId: string,
    projectSprint: string,
    uploadedBy: string,
  ): Observable<IngestResponse> {
    const form = new FormData();
    form.append('file', file);
    form.append('project_id', projectId);
    if (projectSprint) form.append('project_sprint', projectSprint);
    if (uploadedBy) form.append('uploaded_by', uploadedBy);
    return this.http.post<IngestResponse>(`${this.base}/ingest/uploads`, form);
  }

  listIngestLogs(skip: number, limit: number): Observable<IngestLog[]> {
    const params = new HttpParams().set('skip', skip).set('limit', limit);
    return this.http.get<IngestLog[]>(`${this.base}/ingest-logs`, { params });
  }
}
