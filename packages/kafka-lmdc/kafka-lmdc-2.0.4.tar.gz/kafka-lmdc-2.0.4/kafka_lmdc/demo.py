import json
from kafka import kafkaAPI

# Os testes estan feitos utilizando a imagen do docker do  Pdf-Extractor
if __name__=="__main__":
    topic_name = "image-detection-sender"
    detections = {'name':"um mensage"}
    kafka_ip = 'localhost:9091'
    test_consumer = False

    # Teste com Comsumer
    if test_consumer:
        c = kafkaAPI.createConsumerWithoutLogin(kafka_ip=kafka_ip, group_id='mygroup-id')
        c.subscribe([topic_name])
        while True:
            msg = c.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print("Consumer error: {}".format(msg.error()))
                continue
            print('Received message: {}'.format(msg.value().decode('utf-8')))
        c.close()
    else:
        # Teste com Producer
        p = kafkaAPI.createProducerWithoutLogin(kafka_ip=kafka_ip, kafka_debug=True)
        json_str = json.dumps(detections)
        p.produce(topic_name, json_str.encode('utf8'))
        p.poll(0)
        p.flush()

    print("Finish.!")