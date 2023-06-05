start:
	docker-compose --env-file .env up --build

format:
	black .
	ruff --fix .

deploy:
	vercel .
