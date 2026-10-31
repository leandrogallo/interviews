.PHONY: up down test test-api test-web logs reset

up:
	docker compose up --build -d
	@echo "API: http://localhost:8000/docs   Web: http://localhost:5173"

down:
	docker compose down

test: test-api test-web

test-api:
	docker compose run --rm api pytest -q

test-web:
	docker compose run --rm --no-deps web sh -c "npm ci --silent && npm test"

logs:
	docker compose logs -f api web

# Borra la base y arranca de cero.
reset:
	docker compose down -v
	$(MAKE) up
