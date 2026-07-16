import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { environment } from '../../../environments/environment';
import { AskResponse } from '../models/models';

/** Talks to Knowledge-Service (the RAG assistant). That service is not built yet, so
 *  callers should handle errors as "assistant unavailable". */
@Injectable({ providedIn: 'root' })
export class KnowledgeService {
  private readonly base = environment.knowledgeApiBaseUrl;

  constructor(private http: HttpClient) {}

  ask(question: string): Observable<AskResponse> {
    return this.http.post<AskResponse>(`${this.base}/ask`, { question });
  }
}
