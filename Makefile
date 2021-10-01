#!make

build:
	docker-compose build

build_no_cache:
	docker-compose build --no-cache

up:
	docker-compose up -d

migrate:
	docker exec volodya_backend python manage.py makemigrations
	docker exec volodya_backend python manage.py migrate

logs_backend:
	docker logs -f volodya_backend

start_bot:
	docker exec volodya_backend python manage.py startbot