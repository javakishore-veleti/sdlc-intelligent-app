import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';

import { UserContextService } from './user-context.service';

/** Attaches the current user's email as X-User-Email on every outgoing request. */
export const userHeaderInterceptor: HttpInterceptorFn = (req, next) => {
  const email = inject(UserContextService).email;
  return next(req.clone({ setHeaders: { 'X-User-Email': email } }));
};
