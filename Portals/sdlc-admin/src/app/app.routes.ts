import { Routes } from '@angular/router';

export const routes: Routes = [
  { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
  {
    path: 'dashboard',
    loadComponent: () =>
      import('./features/dashboard/dashboard.component').then((m) => m.DashboardComponent),
  },
  {
    path: 'entitlements',
    loadComponent: () =>
      import('./features/entitlements/entitlements.component').then((m) => m.EntitlementsComponent),
    children: [
      { path: '', redirectTo: 'users', pathMatch: 'full' },
      {
        path: 'users',
        loadComponent: () =>
          import('./features/entitlements/users/users.component').then((m) => m.UsersComponent),
      },
    ],
  },
  {
    path: 'projects',
    loadComponent: () =>
      import('./features/projects/projects.component').then((m) => m.ProjectsComponent),
    children: [
      { path: '', redirectTo: 'list', pathMatch: 'full' },
      {
        path: 'list',
        loadComponent: () =>
          import('./features/projects/projects-list/projects-list.component').then(
            (m) => m.ProjectsListComponent,
          ),
      },
      {
        path: 'dependencies',
        loadComponent: () =>
          import('./features/projects/project-dependencies/project-dependencies.component').then(
            (m) => m.ProjectDependenciesComponent,
          ),
      },
      {
        path: 'tech-stack',
        loadComponent: () =>
          import('./features/projects/project-tech-stack/project-tech-stack.component').then(
            (m) => m.ProjectTechStackComponent,
          ),
      },
    ],
  },
  { path: '**', redirectTo: 'dashboard' },
];
