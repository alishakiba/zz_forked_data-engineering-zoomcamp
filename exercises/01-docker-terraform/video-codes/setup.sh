docker build \
    -t nyc-data-ingest:v1 .
docker run \
    --name pg-db \
    -e POSTGRES_PASSWORD=123 \
    -p 5432:5432 -d postgres:13
docker run \
  --network host \
  nyc-data-ingest:v1 \
  --user postgres \
  --password 123 \
  --host 127.0.0.1 \
  --port 5432 \
  --db postgres \
  --table_name yellow_taxi_data \
  --url "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"
docker compose up -d
docker compose rm -f
