test_all:
	@for dir in dagster_essentials dagster_and_dbt dagster_testing dagster_and_etl; do \
		( cd dagster_university/$$dir && uv run pytest $${dir}_tests -p no:warnings ); \
	done