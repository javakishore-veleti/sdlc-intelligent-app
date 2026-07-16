export interface Employee {
  id: string;
  first_name: string;
  last_name: string;
  email: string;
  title?: string | null;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface Project {
  id: string;
  name: string;
  code?: string | null;
  description?: string | null;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface ProjectDependency {
  id: string;
  project_id: string;
  depends_on_project_id: string;
  depends_on_capability_id?: string | null;
  group_id?: string | null;
  description?: string | null;
  created_at: string;
  updated_at: string;
}

export interface ProjectTechStack {
  id: string;
  project_id: string;
  name: string;
  category: string;
  version?: string | null;
  created_at: string;
  updated_at: string;
}

export interface TechStackStat {
  name: string;
  project_count: number;
}

export interface DashboardStats {
  project_count: number;
  top_tech_stacks: TechStackStat[];
  generated_at: string;
  cache_ttl_seconds: number;
}
