run:
	@export $$(grep -v '^#' .env | xargs) && uv run uvicorn fraudapi.main:app --host $$HOST --port $$PORT --reload