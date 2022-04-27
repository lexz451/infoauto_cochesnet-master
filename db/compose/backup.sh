#!/bin/sh

echo "$MYSQL_ROOT_PASSWORD"
echo "$MYSQL_DATABASE"

/usr/bin/mysqldump -u root --password="$MYSQL_ROOT_PASSWORD" "$MYSQL_DATABASE" > /sql/backup.sql