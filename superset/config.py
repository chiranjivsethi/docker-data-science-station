# Superset Configuration
# This file extends the default Superset configuration with project-specific settings

import os
from superset.config import *  # noqa: F401, F403

# ============================================================================
# DATABASE CONFIGURATION
# ============================================================================
# The database URI is set via environment variable SQLALCHEMY_DATABASE_URI
# in docker-compose.yml, no changes needed here.

# ============================================================================
# REDIS CONFIGURATION
# ============================================================================
# Cache and celery use shared Redis instance from docker-data-science-station
REDIS_HOST = os.environ.get("CACHE_REDIS_HOST", "redis")
REDIS_PORT = int(os.environ.get("CACHE_REDIS_PORT", 6379))

# ============================================================================
# CACHING
# ============================================================================
# Use Redis for caching (configured via environment variables)
# Default config from docker-compose.yml environment variables should apply

# ============================================================================
# FEATURE FLAGS
# ============================================================================
FEATURE_FLAGS = {
    # Enable advanced data types (timestamps, arrays, etc.)
    "ENABLE_ADVANCED_DATA_TYPES": True,
    
    # Enable versioned exports of charts/dashboards
    "VERSIONED_EXPORT": True,
    
    # Enable experimental UI features
    "DASHBOARD_RBAC": True,
    
    # Enable drill down functionality
    "ALLOW_FULL_CSV_EXPORT": True,
    
    # Enable alerts and reports
    "ALERT_REPORT_LOG_RETENTION": 30,
    
    # Enable chart data cache
    "CHART_CACHE_TIMEOUT": 300,
    
    # Enable SQL Lab features
    "ENABLE_ROW_LEVEL_SECURITY": False,
    
    # Allow table upload from CSV
    "ALLOW_CSV_UPLOAD": True,
}

# ============================================================================
# SECURITY
# ============================================================================
# Secret key is set via environment variable SUPERSET_SECRET_KEY
# Ensure it's set to a strong random value in production

# ============================================================================
# AUTHENTICATION
# ============================================================================
# Using default authentication (database authentication)
# Can be extended to support OAuth, LDAP, etc.

# ============================================================================
# LOGGING
# ============================================================================
LOGGING_CONFIGURATOR = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["console"],
    },
}

# ============================================================================
# DATA SOURCE CONFIGURATION
# ============================================================================
# Predefined connections to other services in the data science station
# Users can add these as data sources in Superset UI

# PostgreSQL - Primary research database
SUPERSET_DATASOURCES = {
    "PostgreSQL - Research DB": {
        "sqlalchemy_uri": "postgresql://postgres:postgres@postgres:5432/research_db",
        "database_name": "research DB",
        "expose_in_sqllab": True,
        "allow_run_async": True,
    },
    "PostgreSQL - Airflow": {
        "sqlalchemy_uri": "postgresql://postgres:postgres@postgres:5432/airflow",
        "database_name": "Airflow Metadata",
        "expose_in_sqllab": False,
        "allow_run_async": False,
    },
    "PostgreSQL - MLflow": {
        "sqlalchemy_uri": "postgresql://postgres:postgres@postgres:5432/mlflow_db",
        "database_name": "MLflow Metadata",
        "expose_in_sqllab": False,
        "allow_run_async": False,
    },
}

# ============================================================================
# UI CUSTOMIZATION
# ============================================================================
# Branding and UI customization
APP_NAME = "Docker Data Science Station"
SUPERSET_WEBSERVER_PORT = 8088
SUPERSET_WEBSERVER_TIMEOUT = 60

# ============================================================================
# PAGINATION
# ============================================================================
ROW_LIMIT = 10000
DISPLAY_MAX_COLUMN = 40

# ============================================================================
# TABLE CONFIGURATION
# ============================================================================
# Timeout for SQL queries (in seconds)
SUPERSET_QUERY_TIMEOUT = 300

# Allow downloads of data
ALLOW_FULL_CSV_EXPORT = True
CSV_DOWNLOAD_TIMEOUT = 120

# ============================================================================
# EMAIL CONFIGURATION (Optional)
# ============================================================================
# For alerts and reports, uncomment and configure:
# SMTP_HOST = os.environ.get("SMTP_HOST", "localhost")
# SMTP_PORT = int(os.environ.get("SMTP_PORT", 25))
# SMTP_STARTTLS = os.environ.get("SMTP_STARTTLS", False)
# SMTP_SSL = os.environ.get("SMTP_SSL", False)
# SMTP_USER = os.environ.get("SMTP_USER")
# SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")
# SUPERSET_EMAIL_SUBJECT_PREFIX = "[Superset] "

# ============================================================================
# EXAMPLES
# ============================================================================
# Don't load example data in production
SUPERSET_LOAD_EXAMPLES = False
