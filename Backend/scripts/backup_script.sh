#!/bin/bash

# Define the backup file path
BACKUP_FILE="/usr/src/app/backups/default.psql.bin"

echo "Backup started at $(date)" >> /usr/src/app/scripts/backup.log

# Remove the old backup file if it exists
if [ -f "$BACKUP_FILE" ]; then
    rm "$BACKUP_FILE"
fi

# Take a new backup
pg_dump -U postgres -h webshop-postgres -F c postgres > "$BACKUP_FILE"

echo "Backup finished at $(date)" >> /usr/src/app/scripts/backup.log
