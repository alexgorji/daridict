.PHONY: dev dev-down

dev:
	docker compose up --build

dev-down:
	docker compose down
