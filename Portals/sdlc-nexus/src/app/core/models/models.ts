export interface Epic {
  id: string;
  project_id: string;
  title: string;
  status: string;
  created_at: string;
}
export interface Feature {
  id: string;
  project_id: string;
  epic_id?: string | null;
  title: string;
  status: string;
}
export interface Sprint {
  id: string;
  project_id: string;
  name: string;
  status: string;
  start_date?: string | null;
  end_date?: string | null;
}
export interface Release {
  id: string;
  project_id: string;
  name: string;
  status: string;
  release_date?: string | null;
}
export interface Story {
  id: string;
  project_id: string;
  title: string;
  status: string;
  story_points?: number | null;
}

export interface IngestLog {
  id: string;
  ref_id: string;
  file_name: string;
  project_sprint?: string | null;
  ingest_type: string;
  storage_type: string;
  ingest_process_status: string;
  ingest_dt?: string | null;
}

export interface IngestResponse {
  ingest_log: IngestLog;
  airflow: { triggered: boolean; dag_run_id?: string | null; detail?: string | null };
}

export interface Citation {
  document?: string;
  application?: string;
  sprint?: string;
  page?: number;
}
export interface AskResponse {
  answer: string;
  citations?: Citation[];
}
