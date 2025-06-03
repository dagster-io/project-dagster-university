test_all:
	@for dir in dagster_essentials dagster_and_dbt dagster_testing dagster_and_etl; do \
		( cd dagster_university/$$dir && uv run pytest $${dir}_tests -p no:warnings ); \
	done

ruff_all:
	@for dir in dagster_essentials dagster_and_dbt dagster_testing dagster_and_etl; do \
		echo "Checking $$dir"; \
		( cd dagster_university/$$dir && \
			uv run ruff check . --select I --fix && \
			uv run ruff check . --fix ); \
	done