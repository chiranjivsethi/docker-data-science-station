# Docker Data Science Station

A comprehensive Docker-based data science environment with Jupyter, Airflow, MinIO, PostgreSQL and Streamlit Dashboard available at http://localhost:80

## Features

- **JupyterLab**: Interactive data analysis and notebook environment
- **Apache Airflow**: Workflow orchestration and DAG management
- **MinIO**: S3-compatible object storage
- **PostgreSQL**: Relational database backend
- **Redis**: Cache and Celery broker for Airflow
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

View logs:
```bash
docker compose logs -f <service_name>
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

View logs for a specific service:
```bash
docker compose logs postgres
docker compose logs jupyterlab
docker compose logs airflow-scheduler
```

## Project Structure

```
docker-data-science-station/
├── docker-compose.yml          # Main orchestration file
├── .env                        # Environment variables
├── README.md                   # This file
├── airflow/
│   └── docker-compose.yml      # Airflow services configuration
├── jupyterlabs/
│   └── dockerfile              # JupyterLab image definition
└── dashboard/
    ├── app.py                  # Streamlit application
    └── dockerfile              # Dashboard image definition
```