docker compose up -d

// Create Topic
docker compose exec broker-1 kafka-topics --create --topic purchases --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1