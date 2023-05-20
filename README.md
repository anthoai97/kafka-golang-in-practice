### Intro
This project using for learn to build an high performance Kafka Streaming Platform.

#### Start Project
```
docker compose up
```

#### Create Kafka Topic 1 - imageUpload
```
docker compose exec broker-1 kafka-topics --create --topic imageUpload --bootstrap-server localhost:9092 --replication-factor 1 --partitions 2
```

#### Install Python - Service
```
python -m pip install -r requirements.txt
```