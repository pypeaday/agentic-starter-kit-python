FROM python:3.12-slim

# Set environment variables
ENV VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

# Install uv
# RUN pip install uv
# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Create a non-root user and set permissions
RUN mkdir -p /app/data && \
    useradd -m appuser && \
    chown -R appuser:appuser /app && \
    chmod 755 /app/data && \
    mkdir -p /opt/venv && \
    chown -R appuser:appuser /opt/venv

# Set working directory
WORKDIR /app

# Copy entrypoint script
COPY --chown=appuser:appuser docker-entrypoint.sh /app/docker-entrypoint.sh
RUN chmod +x /app/docker-entrypoint.sh

# Copy the rest of the application
COPY --chown=appuser:appuser . .

USER appuser
# Create and activate virtual environment
RUN uv venv $VIRTUAL_ENV
ENV UV_PYTHON=$VIRTUAL_ENV/bin/python

# Install dependencies using uv in the virtual environment
RUN uv sync --active

# Expose port
EXPOSE 8000

# Use entrypoint script
ENTRYPOINT ["/app/docker-entrypoint.sh"]
