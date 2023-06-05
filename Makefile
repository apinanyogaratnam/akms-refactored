start:
	docker-compose --env-file .env up --build

format:
	ruff --fix .
	black .
