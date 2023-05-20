### Intro
This project using for learn to build an high performance Kafka Streaming Platform.

#### Start Project
```
docker compose up -d
```

#### Create Kafka Topic
```
docker compose exec broker-1 kafka-topics --create --topic purchases --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1
```

#### Install Python - Service
```
python -m pip install -r requirements.txt
```