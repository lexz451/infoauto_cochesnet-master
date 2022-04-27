#!/bin/sh

cat /sql/backup.sql |  /usr/bin/mysql -u root --password="$MYSQL_ROOT_PASSWORD" "$MYSQL_DATABASE"