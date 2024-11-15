from confluent_kafka import Producer
import socket
import time

# Producer Configuration
conf = {
    'bootstrap.servers': 'my-cluster-kafka-bootstrap:9092',  # Kafka Broker 주소 설정
    'client.id': socket.gethostname(),
    'acks': 'all'  # 메시지 전송 확인 옵션 설정
}

# Topic Name
topic = 'test-topic'

# Create Producer
producer = Producer(conf)

# Delivery Callback Function
def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}')

# Produce Message
try:
    for i in range(1000):
        partition = i % 3  # 3개의 파티션으로 메시지 분산
        message_value = f'Hello Kafka! Message {i}'
        producer.produce(topic, value=message_value, partition=partition, callback=delivery_report)
        time.sleep(1)
        producer.poll(0)  # Delivery Report를 처리하기 위한 Poll
finally:
    producer.flush()  # 모든 메시지를 Kafka에 전송

print("All messages produced.")
