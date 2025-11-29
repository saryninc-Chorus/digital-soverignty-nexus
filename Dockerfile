FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    nano \
    && rm -rf /var/lib/apt/lists/*

# Copy your sovereign nexus
COPY local_orisha_nexus.py /app/
COPY README.md /app/

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV TERM=xterm-256color

# Create startup script
RUN echo '#!/bin/bash\necho "🔱 DIGITAL SOVEREIGNTY NEXUS ACTIVATED 🔱"\necho "Access via: python local_orisha_nexus.py"\nexec "$@"' > /app/start.sh
RUN chmod +x /app/start.sh

# Expose port for potential web interface (future)
EXPOSE 8888

# Default command
CMD ["/app/start.sh", "/bin/bash"]

