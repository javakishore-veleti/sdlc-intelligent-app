export const environment = {
  production: false,
  // Backend service base URLs.
  workspaceApiBaseUrl: 'http://localhost:8002/api/v1', // Workspace-Service (per-user scoped)
  ingestApiBaseUrl: 'http://localhost:8003/api/v1', // Ingest-Extract-Service
  knowledgeApiBaseUrl: 'http://localhost:8004/api/v1', // Knowledge-Service (not built yet)
};
