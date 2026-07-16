# infra

Local Docker stack for the SDLC Intelligent App. Reuses images already present on the
machine (`pull_policy: missing` → won't re-pull when the tag exists locally).

## Bring up / down

```bash
cicd/Local/docker-all-up.sh        # build + start everything (detached)
cicd/Local/docker-all-status.sh    # container status
cicd/Local/docker-all-down.sh      # stop & remove (add --volumes to wipe data)
```

## Services & ports

| Service | Image | Port | Notes |
|---|---|---|---|
| **postgres** | `postgres:16` | 5432 | creates `master_data` + `airflow` DBs on first init |
| **chromadb** | `chromadb/chroma:latest` | 8000 | vector DB (ingestion target) |
| **master-data-service** | built from `Middleware/Master-Data-Service` | 8001 | `/docs` for Swagger; migrations auto-run on startup |
| **airflow-webserver** | `apache/airflow:2.10.0-python3.12` | 8080 | UI (admin/admin); DAGs from `Middleware/SDLC-Workflows` |
| **airflow-scheduler** | `apache/airflow:2.10.0-python3.12` | — | LocalExecutor |
| **pgadmin** | `dpage/pgadmin4:8.12` | 5050 | admin@example.com / admin |

## Notes

- **Airflow DAGs** are mounted from `Middleware/SDLC-Workflows` → `/opt/airflow/dags`.
- **Airflow permissions:** on Linux, export `AIRFLOW_UID=$(id -u)` before bringing the
  stack up so mounted log files are owned correctly. On macOS the default is fine.
- **Kafka** is intentionally not included yet (added when an event-driven service needs it).
- Postgres credentials (dev only): `sdlc` / `sdlc`.
