# Docker Data Science Station

## Environment Configuration

### Setup

Edit `.env` and update with your own values:
```bash
JUPYTER_TOKEN=your_secure_token_here
RESEARCH_DIR=/path/to/your/research/data
HOST_PORT=8888
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
```