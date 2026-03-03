# ============ Stage 1: Builder ============
FROM python:3.12-slim AS builder

WORKDIR /app

# Install system dependencies for building psycopg2
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies into a separate prefix
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ============ Stage 2: Production ============
FROM python:3.12-slim AS production

# Create non-root user
RUN groupadd -r appuser && \
    useradd -r -g appuser -d /app -s /sbin/nologin appuser

WORKDIR /app

# Install only runtime dependencies (libpq for PostgreSQL)
RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq5 && \
    rm -rf /var/lib/apt/lists/*

# Copy installed Python packages from builder stage
COPY --from=builder /install /usr/local

# Copy application code
COPY . .

# Collect static files at build time
RUN SECRET_KEY=build-placeholder \
    DATABASE_URL=sqlite:///placeholder.db \
    DEBUG=True \
    python manage.py collectstatic --noinput 2>/dev/null || true

# Create necessary directories and set ownership
RUN mkdir -p /app/media /app/staticfiles && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "3", \
     "--timeout", "120", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]
