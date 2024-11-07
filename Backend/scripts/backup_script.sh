#!/bin/bash

# تنظیم متغیر محیطی رمزعبور برای pg_dump
export PGPASSWORD="postgres"

# ایجاد نام فایل بکاپ با زمان‌سنجی
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="/usr/src/app/backups/default_$TIMESTAMP.psql.bin"

# ثبت زمان شروع بکاپ در لاگ
echo "Backup started at $(date)" >> /usr/src/app/scripts/backup.log

# حذف بکاپ قدیمی در صورت وجود
if [ -f "$BACKUP_FILE" ]; then
    rm "$BACKUP_FILE"
fi

# اجرای pg_dump با مسیر کامل و ایجاد بکاپ
/usr/bin/pg_dump -U postgres -h webshop-postgres -F c postgres > "$BACKUP_FILE"

# بررسی موفقیت‌آمیز بودن بکاپ
if [ $? -eq 0 ]; then
    echo "Backup finished at $(date)" >> /usr/src/app/scripts/backup.log
    echo "Backup file created: $BACKUP_FILE" >> /usr/src/app/scripts/backup.log
else
    echo "Backup failed at $(date)" >> /usr/src/app/scripts/backup.log
fi
