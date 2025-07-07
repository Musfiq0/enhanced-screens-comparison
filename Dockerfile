# Enhanced Screenshot Comparison Tool - Docker Container
# Multi-stage build for optimized container size

# Build stage
FROM python:3.9-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Runtime stage
FROM python:3.9-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    # GUI libraries (for X11 forwarding)
    python3-tk \
    x11-apps \
    # Video processing libraries
    libopencv-dev \
    ffmpeg \
    # Additional libraries that might be needed
    libgtk-3-0 \
    libgstreamer1.0-0 \
    libgstreamer-plugins-base1.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder
COPY --from=builder /root/.local /root/.local

# Set working directory
WORKDIR /app

# Copy application code
COPY . .

# Create non-root user for security
RUN useradd -m -s /bin/bash appuser && \
    chown -R appuser:appuser /app
USER appuser

# Add local packages to PATH
ENV PATH=/root/.local/bin:$PATH

# Create output directory
RUN mkdir -p Screenshots

# Set environment variables
ENV PYTHONPATH=/app
ENV DISPLAY=:0

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Default command - show help
CMD ["python", "comparev2.py", "--help"]

# Labels for metadata
LABEL maintainer="Enhanced Screenshot Comparison Tool"
LABEL description="Cross-platform video screenshot comparison tool"
LABEL version="3.2"
LABEL org.opencontainers.image.source="https://github.com/YourUsername/enhanced-screens-comparison"
