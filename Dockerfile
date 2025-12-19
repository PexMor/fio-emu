FROM python:3.13-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    bash \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install --no-cache-dir uv

# Set working directory
WORKDIR /app

# Copy dependency files and README (needed for package build)
COPY pyproject.toml uv.lock README.md ./

# Copy source code (needed for uv sync to build the package)
COPY fioemu/ ./fioemu/

# Install dependencies and the package using uv
RUN uv sync --frozen

# Copy remaining files (scripts, docs, etc.)
COPY r01_make_inject.sh ./

# Default command (can be overridden)
CMD ["uv", "run", "fioemu", "--host", "0.0.0.0", "--port", "8080"]
