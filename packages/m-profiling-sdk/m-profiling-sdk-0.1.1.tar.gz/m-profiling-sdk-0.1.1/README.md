- **Thư viện Consumer của Profiling** :
* Tự động tạo kafka topics
```python
from mobio.libs.kafka_consumer_lib.helpers.ensure_kafka_topic import create_kafka_topics
create_kafka_topics(['test1'])
```
* Kafka Python Consumer
    
```python
from mobio.libs.kafka_consumer_lib.helpers.kafka_python_consumer_manager_v2 import KafkaPythonConsumerManagerV2, KafkaPythonMessageQueue
from mobio.libs.kafka_consumer_lib import ConsumerGroup
import os
from pymongo import MongoClient

# Đây là function khởi tạo client-mongo
def create_db():
    print("create_db: ok")

    try:
        url_connection = os.getenv('PROFILING_MONGODB_URI')
        client = MongoClient(url_connection, connect=False)
    except Exception as ex:
        print('ERROR BaseModel::create_db: %r', ex)
        client = None

    return client

# Đây là class xử lý message
class KafkaPythonConsumer(KafkaPythonMessageQueue):
    def __init__(self, mongo_client, topic_name, num_worker, group_id):
        super().__init__(mongo_client, topic_name, num_worker, group_id)

    def process_msg(self, payload):
        try:
            print('payload: {}'.format(payload))
        except Exception as e:
            print("ThreadMergeConsumer::ERR: {}".format(e))

# Đây là function khởi tạo consumers
def start_kafka_python():
    mongo_client = create_db()
    # FORMAT: CLASS, CLIENT-MONGO, TOPIC, NUMBER_CONSUMER, GROUP_NAME
    consumer_list = [(KafkaPythonConsumer, mongo_client, 'test1', 1, ConsumerGroup.DEFAULT_CONSUMER_GROUP_ID)]

    if consumer_list:
        manager = KafkaPythonConsumerManagerV2(consumer_list)
if __name__ == "__main__":
    start_kafka_python()
```
    
* Confluent Kafka Consumer

```python
import os
from mobio.libs.kafka_consumer_lib import ConsumerGroup
from pymongo import MongoClient 
from mobio.libs.kafka_consumer_lib.helpers.confulent_consumer_manager import ConfluentConsumerManager, ConfluentMessageQueue

# Đây là function khởi tạo client-mongo
def create_db():
    print("create_db: ok")

    try:
        url_connection = os.getenv('PROFILING_MONGODB_URI')
        client = MongoClient(url_connection, connect=False)
    except Exception as ex:
        print('ERROR BaseModel::create_db: %r', ex)
        client = None

    return client

class ConfluentKafkaConsumer(ConfluentMessageQueue):

    def __init__(self, mongo_client, topic_name, num_worker, group_id):
        super().__init__(mongo_client, topic_name, num_worker, group_id)

    def process_msg(self, payload):
        print('payload: {}'.format(payload))
        raise Exception('test')

def start_confluent_consumer():
    mongo_client = create_db()
    consumer_list = [(ConfluentKafkaConsumer, mongo_client, 'test1', 1, ConsumerGroup.DEFAULT_CONSUMER_GROUP_ID)]

    if consumer_list:
        manager = ConfluentConsumerManager(consumer_list)


if __name__ == "__main__":
    # test_create_topic()
    # start_kafka_python()
    start_confluent_consumer()
```
        
** Update version 0.1.1
* support Enable/Disable retry consumer