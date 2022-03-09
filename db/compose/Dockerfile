FROM mariadb:10.4

COPY ./compose/backup.sh /backup
RUN sed -i 's/\r//' /backup
RUN chmod +x /backup

COPY ./compose/restore.sh /restore
RUN sed -i 's/\r//' /restore
RUN chmod +x /restore



