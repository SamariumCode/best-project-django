FROM python:3.10-slim

# Prevent Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE 1

# Prevent Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /usr/src/app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    postgresql-client \
    cron \
    nano \
    && rm -rf /var/lib/apt/lists/*

# Copy only the requirements file first to leverage Docker cache
COPY requirements.txt .

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the project files into the container
COPY . .

# Expose port 8000
EXPOSE 8000

# Add your backup script and set permissions
COPY scripts/backup_script.sh /usr/src/app/backup_script.sh
RUN chmod +x /usr/src/app/backup_script.sh

# Set up the cron job
COPY scripts/mycron /etc/cron.d/mycron
RUN chmod 0644 /etc/cron.d/mycron && \
    crontab /etc/cron.d/mycron

# Start both cron and gunicorn in the same command
CMD ["sh", "-c", "cron -f && gunicorn --bind 0.0.0.0:8000 config.wsgi:application"]
