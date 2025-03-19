#/bin/bash
set -x

ENDPOINT_URL='http://localhost:4566'

aws --endpoint-url=$ENDPOINT_URL s3 mb s3://dagster
aws --endpoint-url=$ENDPOINT_URL s3 cp data/test.csv s3://dagster/test/file_1.csv
aws --endpoint-url=$ENDPOINT_URL s3 cp data/test.csv s3://dagster/test/file_2.csv
aws --endpoint-url=$ENDPOINT_URL s3 cp data/test.csv s3://dagster/test/file_3.csv