import logging
from applauncher.kernel import Configuration, Kernel, ConfigurationReadyEvent, KernelShutdownEvent, InjectorReadyEvent
import inject
from confluent_kafka import Producer, Consumer

class KafkaException(Exception):
    pass

def delivery_callback(err, msg):
    if err:
        raise KafkaException(err)

class KafkaManager(object):
    def __init__(self, config):
        self.config = config
        self.default_producer = self.get_producer()
        self.kernel = None
        self.run = True

    def produce(self, topic, message, headers=None, flush=False):
        self.default_producer.produce(topic, message, headers=headers, callback=delivery_callback)
        if flush:
            self.default_producer.flush()

    def subscribe(self, topics, group_id, consumer_callback, poll_timeout=1):
        self.kernel.run_service(
            self._subscribe_service,
            topics,
            group_id,
            consumer_callback,
            poll_timeout
        )

    def _subscribe_service(self, topics, group_id, consumer_callback, poll_timeout):
        consumer = self.get_consumer(group_id=group_id)  # type: Consumer
        consumer.subscribe(topics=topics)
        logging.info("Subscribed to {topics}".format(topics=",".join(topics)))
        while self.run:
            try:
                msg = consumer.poll(timeout=poll_timeout)
                if msg is None:
                    continue

                if msg.error():
                    error = msg.error()
                    raise KafkaException("Error {error_code}: {error}".format(error_code=error.code(), error=str(error)))

                try:
                    consumer_callback(msg)
                except Exception as e:
                    logging.error(f"Consumer error {str(e)}")
            except Exception as e:
                logging.error(str(e))


    def get_producer(self):
        return Producer(**self.config)

    def get_consumer(self, group_id):
        c = dict(self.config)
        c["group.id"] = group_id
        return Consumer(**c)


def applauncher_config_to_confluent(config):
    c = {}
    for k, v in config._asdict().items():
        k = k.replace("_", ".")
        if v.__class__.__name__ == "Configuration":
            c[k] = applauncher_config_to_confluent(v)
        else:
            c[k] = v
    if "bootstrap.servers" in c:
        if c["bootstrap.servers"].startswith("sasl://"):
            # sasl://username:password@servers
            credentials, servers = c["bootstrap.servers"][7:].split("@")
            username, password = credentials.split(":")
            c["bootstrap.servers"] = servers
            c["sasl.username"] = username
            c["sasl.password"] = password

    return c


class KafkaBundle(object):
    def __init__(self):
        self.logger = logging.getLogger("kafka")
        self.config_mapping = {
            "kafka": {
                'bootstrap_servers': None,
                'session_timeout_ms': 6000,
                'default_topic_config': {'auto_offset_reset': 'earliest'},
                'security_protocol': 'SASL_SSL',
                'sasl_mechanisms': 'SCRAM-SHA-256',
                'partition_assignment_strategy': 'roundrobin',
                'sasl_username': '',
                'sasl_password': ''
            }
        }

        self.event_listeners = [
            (ConfigurationReadyEvent, self.config_ready),
            (InjectorReadyEvent, self.injector_ready),
            (KernelShutdownEvent, self.shutdown),
        ]

        self.injection_bindings = {}

    @inject.params(kernel=Kernel, kafka=KafkaManager)
    def injector_ready(self, event, kernel, kafka):
        kafka.kernel = kernel

    def config_ready(self, event):
        kafka_config = applauncher_config_to_confluent(event.configuration.kafka)
        self.injection_bindings[KafkaManager] = KafkaManager(kafka_config)

    @inject.params(kafka=KafkaManager)
    def shutdown(self, event, kafka: KafkaManager):
        kafka.run = False
        kafka.default_producer.flush()
