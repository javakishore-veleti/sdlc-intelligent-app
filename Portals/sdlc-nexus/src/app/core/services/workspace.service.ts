import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { environment } from '../../../environments/environment';
import { Epic, Feature, Release, Sprint, Story } from '../models/models';

@Injectable({ providedIn: 'root' })
export class WorkspaceService {
  private readonly base = environment.workspaceApiBaseUrl;

  constructor(private http: HttpClient) {}

  private page(skip: number, limit: number): HttpParams {
    return new HttpParams().set('skip', skip).set('limit', limit);
  }

  getEpics(skip: number, limit: number): Observable<Epic[]> {
    return this.http.get<Epic[]>(`${this.base}/epics`, { params: this.page(skip, limit) });
  }
  getFeatures(skip: number, limit: number): Observable<Feature[]> {
    return this.http.get<Feature[]>(`${this.base}/features`, { params: this.page(skip, limit) });
  }
  getSprints(skip: number, limit: number): Observable<Sprint[]> {
    return this.http.get<Sprint[]>(`${this.base}/sprints`, { params: this.page(skip, limit) });
  }
  getReleases(skip: number, limit: number): Observable<Release[]> {
    return this.http.get<Release[]>(`${this.base}/releases`, { params: this.page(skip, limit) });
  }
  getStories(skip: number, limit: number): Observable<Story[]> {
    return this.http.get<Story[]>(`${this.base}/stories`, { params: this.page(skip, limit) });
  }
}
