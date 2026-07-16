import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

/**
 * Holds the "signed-in" user email. A stand-in for real authentication: its value is
 * attached as the X-User-Email header on every request (see user-header.interceptor),
 * which is what Workspace-Service uses to scope data per user (admins see all).
 */
@Injectable({ providedIn: 'root' })
export class UserContextService {
  private readonly _email$ = new BehaviorSubject<string>('demo@example.com');
  readonly email$ = this._email$.asObservable();

  get email(): string {
    return this._email$.value;
  }

  setEmail(email: string): void {
    this._email$.next((email || '').trim() || 'demo@example.com');
  }
}
