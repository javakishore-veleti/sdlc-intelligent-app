"""Service-wide constants."""
import os

SERVICE_NAME = "Master-Data-Service"
SERVICE_VERSION = "0.1.0"

API_V1_PREFIX = "/api/v1"

DEFAULT_PAGE_SIZE = 100
MAX_PAGE_SIZE = 1000

# Dashboard stats cache eviction window (seconds). Default 6 hours; override with
# the DASHBOARD_CACHE_TTL_SECONDS environment variable.
DASHBOARD_CACHE_TTL_SECONDS = int(os.getenv("DASHBOARD_CACHE_TTL_SECONDS", str(6 * 60 * 60)))
