import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { environment } from '../../../environments/environment';
import {
  DashboardStats,
  Employee,
  Project,
  ProjectDependency,
  ProjectTechStack,
} from '../models/master-data.models';

@Injectable({ providedIn: 'root' })
export class MasterDataService {
  private readonly base = environment.masterDataApiBaseUrl;

  constructor(private http: HttpClient) {}

  private page(skip: number, limit: number): HttpParams {
    return new HttpParams().set('skip', skip).set('limit', limit);
  }

  getEmployees(skip: number, limit: number): Observable<Employee[]> {
    return this.http.get<Employee[]>(`${this.base}/employees`, { params: this.page(skip, limit) });
  }

  getProjects(skip: number, limit: number): Observable<Project[]> {
    return this.http.get<Project[]>(`${this.base}/projects`, { params: this.page(skip, limit) });
  }

  getProjectDependencies(skip: number, limit: number): Observable<ProjectDependency[]> {
    return this.http.get<ProjectDependency[]>(`${this.base}/project-dependencies`, {
      params: this.page(skip, limit),
    });
  }

  getProjectTechStacks(skip: number, limit: number): Observable<ProjectTechStack[]> {
    return this.http.get<ProjectTechStack[]>(`${this.base}/project-tech-stacks`, {
      params: this.page(skip, limit),
    });
  }

  getDashboardStats(): Observable<DashboardStats> {
    return this.http.get<DashboardStats>(`${this.base}/dashboard/stats`);
  }
}
