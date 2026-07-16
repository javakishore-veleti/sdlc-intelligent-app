import { Routes } from '@angular/router';

export const routes: Routes = [
  { path: '', redirectTo: 'workspace', pathMatch: 'full' },
  {
    path: 'workspace',
    loadComponent: () =>
      import('./features/workspace/workspace.component').then((m) => m.WorkspaceComponent),
  },
  {
    path: 'upload',
    loadComponent: () =>
      import('./features/upload/upload.component').then((m) => m.UploadComponent),
  },
  {
    path: 'assistant',
    loadComponent: () =>
      import('./features/assistant/assistant.component').then((m) => m.AssistantComponent),
  },
  { path: '**', redirectTo: 'workspace' },
];
