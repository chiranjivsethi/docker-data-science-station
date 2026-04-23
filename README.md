# Docker Data Science Station

A comprehensive Docker-based data science environment with JupyterLab, Apache Airflow, MLflow, MinIO, PostgreSQL, Apache Superset, and Streamlit Dashboard available at http://localhost:80

## Features

- **JupyterLab**: Interactive data analysis and notebook environment
- **Apache Airflow**: Workflow orchestration and DAG management
- **MinIO**: S3-compatible object storage
- **PostgreSQL**: Relational database backend
- **Redis**: Cache and Celery broker for Airflow
- **MLflow**: Machine learning experiment tracking and model registry
- **Apache Superset**: Interactive data visualization and BI layer
- **Streamlit Dashboard**: Unified access layer for all services
- **Automatic Directory Creation**: All required directories are created on first run for reproducibility


## Docker Commands

Start services:
```bash
docker compose up -d
```

Stop services:
```bash
docker compose down
```

View service logs:
```bash
docker compose logs -f <service_name>
```

View all running services:
```bash
docker compose ps
```

## Jupyter Kernel Management

Install a new kernel:
```bash
uv run python -m ipykernel install --user --name="<kernelname>" --display-name="<kernelsidpayname>"
```

List installed kernels:
```bash
jupyter kernelspec list
```

Uninstall a kernel:
```bash
jupyter kernelspec uninstall <kernelname>
```

## Services & Access Ports

| Service | Port | URL | Purpose |
|---------|------|-----|---------|
| **Streamlit Dashboard** | 80 | http://localhost:80 | Unified access layer & service monitoring |
| **JupyterLab** | 8888 | http://localhost:8888 | Interactive data analysis & notebook environment |
| **MinIO Console** | 9001 | http://localhost:9001 | Object storage management & S3 buckets |
| **PostgreSQL** | 5432 | postgresql://localhost:5432 | Relational database backend |
| **Apache Airflow** | 8080 | http://localhost:8080 | Workflow orchestration & DAG management |
| **MLflow** | 5000 | http://localhost:5000 | ML experiment tracking & model registry |
| **Apache Superset** | 8088 | http://localhost:8088 | Interactive BI & data visualization |

## Apache Superset Setup

Apache Superset provides a modern data visualization and business intelligence platform integrated into the data science station.

### Access Superset

- **URL**: http://localhost:8088
- **Default Credentials**: 
  - Username: `admin` (configurable via `SUPERSET_ADMIN_USER` in .env)
  - Password: `admin` (configurable via `SUPERSET_ADMIN_PASSWORD` in .env)

⚠️ **Security Note**: Change the default credentials in production by updating `.env` variables:
- `SUPERSET_ADMIN_USER`
- `SUPERSET_ADMIN_PASSWORD`
- `SUPERSET_ADMIN_EMAIL`
- `SUPERSET_SECRET_KEY` (generate with: `python -c "import secrets; print(secrets.token_hex(32))"`)

### Superset Data Sources

Superset is pre-configured with access to:

1. **PostgreSQL - Research DB** (Primary Database)
   - Host: `postgres:5432`
   - Database: `research_db`
   - Credentials: From `.env` (`POSTGRES_USER`, `POSTGRES_PASSWORD`)
   - Purpose: Main research and analysis data

2. **PostgreSQL - Airflow Metadata** (Read-only)
   - Host: `postgres:5432`
   - Database: `airflow`
   - Purpose: View Airflow DAG execution history and metrics

3. **PostgreSQL - MLflow Metadata** (Read-only)
   - Host: `postgres:5432`
   - Database: `mlflow_db`
   - Purpose: Access MLflow experiment tracking data

4. **MinIO/S3 Storage** (Configurable)
   - Endpoint: `http://minio:9000`
   - Credentials: From `.env` (`MINIO_ROOT_USER`, `MINIO_ROOT_PASSWORD`)
   - Purpose: Direct access to object storage for data analysis

### Creating Data Sources in Superset

1. Navigate to **Settings → Database Connections**
2. Click **+ Database**
3. Select your database type (PostgreSQL, S3, etc.)
4. Fill in connection details:
   - For PostgreSQL: Use service names (`postgres`) as hostname
   - For S3: Use MinIO endpoint with appropriate credentials
5. Test connection and save

### Redis Caching

Superset uses the shared Redis instance (`redis:6379`) for:
- Query result caching (performance optimization)
- Session management
- Celery task queuing (for async report generation)

This ensures fast dashboard load times and smooth user experience.

## Troubleshooting

### Directories Not Created

If directories are not created automatically, ensure:
1. The `.env` file has the correct paths
2. You have write permissions on the parent directories
3. Run `docker compose up -d` from the root project directory

### Permission Issues

If you encounter permission errors on mounted volumes:
```bash

sudo chmod -R 777 /to/directory/path
```

### Service Health

Check service status:
```bash
docker compose ps
```

All services should show "Up" status. If any service is not running, check logs:
```bash
docker compose logs <service_name>
```

### Superset Initialization Issues

If Superset fails to start or initialize:

1. **Check database migration**: Superset needs to run database migrations on first start
   ```bash
   docker compose logs superset | grep -i "database\|migration"
   ```

2. **Verify PostgreSQL is healthy**: Superset depends on PostgreSQL `superset_db` database
   ```bash
   docker compose exec postgres psql -U postgres -lc | grep superset_db
   ```

3. **Reset Superset admin user** (if credentials forgotten):
   ```bash
   docker compose exec superset superset fab create-admin \
     --username admin \
     --firstname Superset \
     --lastname Admin \
     --email admin@example.com \
     --password admin
   ```

### Connecting to Services from Containers

When connecting to services from within containers (e.g., from Airflow DAGs):
- Use service names instead of `localhost`: `postgres`, `minio`, `redis`, `superset`, etc.
- Services are on the shared `data_science_network` bridge network
- Example PostgreSQL connection string from container: `postgresql://postgres:postgres@postgres:5432/research_db`

## Project Structure

```
docker-data-science-station/
├── docker-compose.yml          # Main orchestration file
├── .env                        # Environment variables (local, not in version control)
├── .env.example                # Environment template with all available options
├── README.md                   # This file
├── airflow/
│   └── docker-compose.yml      # Airflow services configuration
├── jupyterlabs/
│   └── dockerfile              # JupyterLab image definition
├── mlflow/
│   └── docker-compose.yml      # MLflow tracking server configuration
├── superset/
│   ├── docker-compose.yml      # Superset services and initialization
│   ├── config.py               # Superset configuration
│   └── .gitignore              # Superset-specific ignores
└── dashboard/
    ├── app.py                  # Streamlit unified dashboard
    └── dockerfile              # Dashboard image definition
```