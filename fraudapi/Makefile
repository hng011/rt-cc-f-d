install:
	@echo installing dev dependencies...
	@uv sync

run:
	@export $$(grep -v '^#' .env | xargs) \
	&& uv run uvicorn app.main:app --host $$HOST --port $$PORT --reload

run-compose:
	docker compose up --build

stop-compopse:
	docker compose down