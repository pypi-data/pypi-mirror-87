from copy import deepcopy
from datetime import datetime, timedelta
import json
import threading
import uuid
from abc import abstractmethod
from threading import Thread
from kafka import KafkaConsumer
from time import time

from mobio.libs.kafka_consumer_lib import ConsumerGroup, RequeueStatus, KAFKA_BOOTSTRAP
from mobio.libs.kafka_consumer_lib.models.mongo.requeue_consumer_model import (
    RequeueConsumerModel,
)


class KafkaPythonConsumerManagerV2:
    def __init__(self, consumer_list):
        # self.arr_workers = Queue(64)
        self.consumer_list = consumer_list
        self.arr_workers = []

        self.init_manager()

    def init_manager(self):
        for cls, client_mongo, topic, worker, group_id, retryable in self.consumer_list:
            self.init_consumer(cls, client_mongo, topic, worker, group_id, retryable)

    def init_consumer(self, cls, client_mongo, topic, num_worker, group_id, retryable):
        consumer = cls(client_mongo, topic, num_worker, group_id, retryable)
        self.arr_workers.append(consumer)
        # self.arr_workers.put(consumer)

    def __del__(self):
        print("ConsumerManager: __del__: ok")
        # for consumer in self.arr_workers:
        #     consumer.start_consumer()


class KafkaPythonMessageQueue:
    def __init__(
        self,
        client_mongo,
        topic_name,
        num_worker,
        group_id=ConsumerGroup.DEFAULT_CONSUMER_GROUP_ID,
        retryable=True,
    ):
        if not group_id:
            group_id = ConsumerGroup.DEFAULT_CONSUMER_GROUP_ID
        self.num_worker = num_worker
        self.topic_name = topic_name
        self.group_id = group_id
        self.client_mongo = client_mongo
        self.thread = []
        self.retryable = retryable

        self.stop_event = threading.Event()
        for i in range(num_worker):
            t = ThreadConsumer(i, self.on_process)
            self.thread += [t]
            t.start()

    def on_process(self):
        print("KafkaPythonMessageQueue: on_process")
        consumer = KafkaConsumer(
            bootstrap_servers=KAFKA_BOOTSTRAP,
            consumer_timeout_ms=3000,
            group_id=self.group_id,
        )
        consumer.subscribe([self.topic_name])

        while not self.stop_event.is_set():
            for msg in consumer:
                count_err = 0
                data = None
                key = msg.key
                try:
                    payload = json.loads(msg.value.decode())
                    data = deepcopy(payload)
                    if "message_id" in payload and type(payload) == dict:
                        message_id = payload.pop("message_id")
                    else:
                        message_id = str(uuid.uuid4())
                    if "count_err" in payload:
                        count_err = payload.pop("count_err")
                    start_time = time()
                    print(
                        "start: {} with message_id: {} start_time: {}".format(
                            self.topic_name, message_id, start_time
                        )
                    )
                    self.process_msg(payload)
                    end_time = time()
                    print(
                        "end: {} with message_id: {} total time: '[{:.3f}s]".format(
                            self.topic_name, message_id, end_time - start_time
                        )
                    )
                except Exception as e:
                    print(
                        "MessageQueue::run - topic: {} ERR: {}".format(
                            self.topic_name, e
                        )
                    )
                    if data and self.retryable:
                        data_error = {
                            "topic": self.topic_name,
                            "key": key.decode('ascii') if key else key,
                            "data": data,
                            "error": str(e),
                            "count_err": count_err + 1,
                            "next_run": datetime.utcnow() + timedelta(minutes=5),
                            "status": RequeueStatus.ENABLE
                            if (count_err + 1) <= 10
                            else RequeueStatus.DISABLE,
                        }
                        RequeueConsumerModel(self.client_mongo).insert(data=data_error)
        consumer.close()

    def start_consumer(self):
        print("MessageQueue: start_consumer")
        for t in self.thread:
            t.join()
        print("ok")

    @abstractmethod
    def process_msg(self, payload):
        raise NotImplementedError("You must implement this function on child class")

    def __del__(self):
        print("MessageQueue: __del__")


class ThreadConsumer(Thread):
    def __init__(self, t_id, func, *args):
        super().__init__()
        self.args = args
        self.func = func
        self.id = t_id
        # self.daemon = True

    def run(self):
        self.func(*self.args)

    def __del__(self):
        print("ThreadConsumer: __del__: ok")


# if __name__ == "__main__":
#
#     class TestConsumer1(MessageQueueV2):
#         def process_msg(self, payload):
#             print("TestConsumer1: process_msg: {}".format(payload))
#             print("TestConsumer1: process_msg: {}".format(type(payload)))
#
#     class TestConsumer2(MessageQueueV2):
#         def process_msg(self, payload):
#             print("TestConsumer2: process_msg: {}".format(payload))
#             print("TestConsumer2: process_msg: {}".format(type(payload)))
#
#     class TestConsumer3(MessageQueueV2):
#         def process_msg(self, payload):
#             print("TestConsumer3: process_msg: {}".format(payload))
#             print("TestConsumer3: process_msg: {}".format(type(payload)))
#
#     # init consumer with class name, topic name and number of worker
#     consumer_list = [
#         (TestConsumer1, "consumer-test-1", 2),
#         (TestConsumer2, "consumer-test-2", 4),
#         (TestConsumer3, "consumer-test-3", 16),
#     ]
#
#     manager = KafkaPythonConsumerManagerV2(consumer_list)
#     # manager.arr_workers.join()
