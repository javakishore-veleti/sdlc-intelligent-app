#!/bin/bash
# Runs once on first Postgres init. Creates the databases used by the stack:
#   - master_data : Master-Data-Service
#   - airflow     : Apache Airflow metadata
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
  CREATE DATABASE master_data;
  CREATE DATABASE airflow;
  CREATE DATABASE ingest;
  CREATE DATABASE workspace;
EOSQL

echo "Created databases: master_data, airflow, ingest, workspace"
