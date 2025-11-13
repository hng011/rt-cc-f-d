install-hooks:
	@echo installing dev packages...
	@uv sync --group dev
	
	@echo installing pre-commit hook...
	@uv run pre-commit install
	
	@echo "--- ✅ Install complete! ---"
	@echo "--- IMPORTANT: Run 'ggshield auth login' manually if this is your first time. ---"