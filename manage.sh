#!/bin/bash

function display_help() {
    cat <<-EOF
      ************************* Sails backend *****************************
      **  Usage: ./manage.sh <command>
      **  Available commands are:
      **    start               Run docker compose up
      **    deploy              Run docker compose up on daemon mode (-d)
      **    migrate             Apply initial or pending database migrations
      **    build               Build docker container images
      **    stop                Stop/Remove docker containers
      **    backup              Backup database
      **    restore             Restore database
      **    create_superuser    Creates the django superuser account
      **    logs <container>    Display container logs
      **    help                Print this help
      *********************************************************************
EOF
}

function wrong_cmd() {
    display_help;
}

function start() {
    P=${1}
    MODE=${P:-"attach"}
    if [ "$MODE" == "attach" ]; then
      echo "Running docker containers...";
      docker-compose up;
    else
      echo "Running docker containers on daemon mode...";
      docker-compose up -d;
    fi
}

function migrate() {
    echo "Migrating database...";
    docker-compose run --rm backend python manage.py makemigrations;
    docker-compose run --rm backend python manage.py migrate;
}

function build() {
    echo "Building docker containers...";
    docker-compose build;
}

function backup() {
    echo "Backing-up database...";
    docker run -v "$(pwd)"_mysql-data:/volume --rm loomchild/volume-backup backup - > ./"$(pwd)"_mysql-data.tar.bz2
}

function restore() {
    echo "Restoring database...";
    # shellcheck disable=SC2002
    cat ./"$(pwd)"_mysql-data.tar.bz2 | docker run -i -v "$(pwd)"_mysql-data:/volume --rm loomchild/volume-backup restore -
}

function create_superuser() {
    echo "Creating superuser...";
    docker-compose run --rm backend python manage.py createsuperuser;
}

function display_logs() {
    CONTAINER=${1};
    echo "Displaying $CONTAINER logs...";
    docker-compose logs -f "$CONTAINER";
}

function stop() {
    echo "Stopping docker containers...";
    docker-compose down;
}

case "$1" in
  start) start;;
  deploy) start "daemon";;
  migrate) migrate;;
  build) build;;
  stop) stop;;
  backup) backup;;
  restore) restore;;
  create-superuser) create_superuser;;
  help) display_help;;
  logs) display_logs "$@";;
  *) wrong_cmd;;
esac