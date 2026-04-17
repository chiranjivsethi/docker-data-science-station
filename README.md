# Docker Data Science Station

## Environment Configuration

### Setup

Edit `.env` and update with your own values:
```bash
# JupyterLab
JUPYTER_TOKEN=your_secure_token_here
RESEARCH_DIR=/path/to/your/research/data
HOST_PORT=8888

# MinIO
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin
MINIO_DATA_DIR=/path/to/minio/data
```

## Docker Commands

Start services:
```bash
docker compose up -d
```

Stop services:
```bash
docker compose down
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

## Accessing CSV Files from MinIO in Jupyter

Install the MinIO client in your Jupyter notebook:
```python
!pip install minio
```

Read CSV files stored in MinIO:
```python
from minio import Minio
import pandas as pd
from io import BytesIO

# Create MinIO client
# Note: Use the service name 'minio_container' as the endpoint since you're in Docker
minio_client = Minio(
    "minio_container:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)

# Read CSV from MinIO bucket
bucket_name = "your-bucket-name"
object_name = "path/to/your/file.csv"

response = minio_client.get_object(bucket_name, object_name)
df = pd.read_csv(BytesIO(response.read()))
```

Access MinIO console at: `http://localhost:9001` (use credentials from `.env`)
```