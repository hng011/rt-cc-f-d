install-dev:
	@echo installing dev dependencies...
	@uv sync --group dev

	@echo installing pre-commit hook...
	@uv run pre-commit install

	@echo "--- ✅ Install complete! ---"
	@echo "--- IMPORTANT: Run 'ggshield auth login' manually if this is your first time. ---"

run-dev:
	@export $$(grep -v '^#' .env | xargs) \
	&& uv run uvicorn app.main:app --host $$HOST --port $$PORT --reload

run-dev-compose:
	docker compose up --build