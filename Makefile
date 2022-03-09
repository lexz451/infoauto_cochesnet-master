.PHONY: help

.DEFAULT_GOAL := help
runner=$(shell whoami)

help: ## This help.
	@echo
	@echo "\e[1;35m Port mapping used: $<\e[0m"
	@echo "\e[1;33m - Backend: localhost:8000 $<\e[0m"
	@echo "\e[1;33m - Frontend: localhost:3000 $<\e[0m"
	@echo "\e[1;33m - Phpmyadmin: localhost:8080 $<\e[0m"
	@echo "\e[1;33m - Celery flower: localhost:5555 $<\e[0m"
	@echo
	@echo "\e[1;36m Testing database credentials in file .envs/.local/.mysql $<\e[0m"
	@echo "\e[1;37m Useful command to backup and restore your database $<\e[0m"
	@echo "\e[1;37m docker exec infoauto-database /usr/bin/mysqldump -u root --password=root infoauto > backup.sql $<\e[0m"
	@echo "\e[1;37m cat ~/backup.sql | docker exec -i infoauto-database /usr/bin/mysql -u root --password=password infoauto $<\e[0m"
	@echo
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo

build: ## Build developer containers.
	docker-compose build

up: down ## Run developer containers.
	docker-compose up

silenceup: ## Run developer containers without print messages.
	docker-compose up -d

createsuperuser: ## Create superuser.
	docker-compose run  --rm backend python manage.py createsuperuser

down: ## Force stop and delete all containers.
	docker-compose down

shell: ## Run django shell.
	docker-compose run  --rm backend python manage.py shell

migrate: ## Run migrate command in django container.
	docker-compose run  --rm backend python manage.py migrate

makemigrations: ## Run makemigrations command in django container.
	docker-compose run  --rm backend python manage.py makemigrations

manage:
	docker-compose run  --rm backend python manage.py $(command)

clean: ## Clean frontend compile files using gulp build
	docker-compose run  --rm frontend gulp clean

compile: clean ## Compile frontend using gulp build
	docker-compose run  --rm frontend gulp build
	sudo chown -R $(runner):$(runner) ./frontend/dist/

djangologs: ## Show and follow the django console messages
	docker-compose logs -f  backend

angularlogs: ## Show and follow the angular console messages
	docker-compose logs -f  frontend

celerylogs: ## Show and follow the celery console messages
	docker-compose logs -f  celeryworker

resetdb: ## Clean database volume.
	docker volume rm $(shell basename $(CURDIR))_mysql-data

backup: ## Create database volume backup.
	@docker run -v $(shell basename $(CURDIR))_mysql-data:/volume --rm loomchild/volume-backup backup - > ./$(shell basename $(CURDIR))_mysql-data.tar.bz2

restore: resetdb  ## Restore database volume backup.
	cat ./$(shell basename $(CURDIR))_mysql-data.tar.bz2 | docker run -i -v $(shell basename $(CURDIR))_mysql-data:/volume --rm loomchild/volume-backup restore -


