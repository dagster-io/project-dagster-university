# AI-driven data engineering

Completed project for the AI-driven data engineering course.

## Local development with MinIO (S3)

The project uses S3 for exporting `fct_orders` (e.g. via Sling) and for asset checks. To run a local MinIO instance:

1. Start MinIO and create the `test-bucket` bucket:
   ```bash
   docker compose up -d
   ```

2. Set S3 credentials and endpoint (e.g. copy from `.env.example` to `.env`):
   ```bash
   cp .env.example .env
   ```
   Then run `dg dev` (or your Dagster command) from this directory; it will read `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `AWS_ENDPOINT_URL_S3` from the environment.
