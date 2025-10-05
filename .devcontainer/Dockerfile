# Dev container base image for autonomous-dev
# Use slim Python image to reduce size; can switch to -bookworm for glibc packages if needed.
FROM mcr.microsoft.com/devcontainers/python:3.11

# Install any OS packages here (kept minimal intentionally)
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential \
#  && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

# Copy only project metadata first for layer caching
COPY pyproject.toml README.md ./

# Pre-create venv path (devcontainers python image already manages .venv)
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    VIRTUAL_ENV=/workspace/.venv \
    PATH=/workspace/.venv/bin:$PATH

# Install dev deps early (will be re-used unless pyproject changes)
RUN python -m venv $VIRTUAL_ENV \
    && pip install --upgrade pip \
    && pip install '.[dev]' || true

# Copy the rest of the source (after deps for caching)
COPY . .

# Reinstall in editable mode with extras to ensure sync
RUN pip install -e '.[dev]' \
    && pre-commit install --install-hooks --overwrite

# Default command (override in devcontainer.json if needed)
CMD ["sleep", "infinity"]
