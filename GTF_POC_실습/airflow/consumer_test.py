from confluent_kafka import Consumer, KafkaException

# Consumer Configuration
conf = {
    'bootstrap.servers': 'my-cluster-kafka-bootstrap:9092',  # Kafka Broker 주소 설정
    'group.id': 'test-group',  # Consumer Group 설정 (같은 group.id를 가진 Consumer는 협력하여 메시지를 소비함)
    'auto.offset.reset': 'earliest'  # Kafka에 메시지 처음부터 소비
}

# Topic Name
topic = 'test-topic'

# Create Consumer
consumer = Consumer(conf)

# Subscribe to the topic
consumer.subscribe([topic])

# Poll for new messages
try:
    while True:
        msg = consumer.poll(1.0)  # 1초 동안 메시지 폴링

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaException._PARTITION_EOF:
                # End of partition event
                print(f"Reached end of partition {msg.partition()}")
            elif msg.error():
                print(f"Error: {msg.error()}")
                break
        else:
            # Proper message
            print(f"Received message: {msg.value().decode('utf-8')} from {msg.topic()} [{msg.partition()}]")
finally:
    # Close consumer
    consumer.close()
