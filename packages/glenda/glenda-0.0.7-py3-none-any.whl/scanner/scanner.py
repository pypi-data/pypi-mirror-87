from confluent_kafka import Consumer, Producer
import os
import logging
import json

module_logger = logging.getLogger("glendaWrapper.Common")


class Common:
    KAFKA_URL = None
    PROGRESS_TOPIC = "start_progress"
    REPORT_TOPIC = "master"

    SCANNER_NAME = ""

    consumer = None
    producer = None

    def __init__(self, scanner_name: str) -> None:
        self.KAFKA_URL = os.getenv("KAFKA_URL", "localhost:9093")
        logging.debug(f"KAFKA_URL {self.KAFKA_URL}")

        self.SCANNER_NAME = scanner_name

        consumer_args = {
            "bootstrap.servers": self.KAFKA_URL,
            "group.id": self.SCANNER_NAME,
            "auto.offset.reset": "earliest",
        }
        self.consumer = Consumer(consumer_args)

        self.producer = Producer({"bootstrap.servers": self.KAFKA_URL})

    def __validate(self, data) -> bool:
        scanner = data.get("scanner_only", self.SCANNER_NAME)
        not_use_scanners = data.get("not_use_scanners", [])

        if self.SCANNER_NAME in not_use_scanners or scanner != self.SCANNER_NAME:
            logging.info("Scanner not use. Skip.")
            return False

        return True

    def __kafka_callback(self, err, msg) -> None:
        """Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush()."""
        if err is not None:
            logging.error("Message delivery failed: {}".format(err))
        else:
            logging.info("Message delivered to {} [{}]".format(msg.topic(), msg.offset()))

    def start(self, data: dict) -> None:
        """
          Отправляем в kafka сообщение о начале сканирования
          data нужна временно. Потом от нее избавимся
          """
        logging.info("Scanner -> Glenda: progress is starting")
        logging.debug(data)

        producer = Producer({"bootstrap.servers": self.KAFKA_URL})
        component = data.get("component", None)

        message = json.dumps({
            "component": component,
            "glenda": self.SCANNER_NAME,
        })

        producer.produce(self.PROGRESS_TOPIC, message.encode("utf-8"), callback=self.__kafka_callback)
        producer.flush()

    def queue(self, queue_name: str, handler):
        """
        Ждем из очереди задачи на скан
        """
        self.consumer.subscribe([queue_name])
        while True:
            message = self.consumer.poll(1.0)
            if message is None:
                continue
            if message.error():
                if "Broker: No more messages" not in str(message.error()):
                    logging.warning("Consumer error: {}".format(message.error()))

                continue
            data = json.loads(message.value())

            logging.info(f"Glenda -> Scanner: get new task for {data.get('project_name', 'undefined')}")
            logging.debug(f"MSG: offset: {message.offset()}, value: {message.value().decode()}")

            if not self.__validate(data):
                continue

            handler(data)

    def result(self, data: list, component: dict, type="default", level="component") -> None:
        """
          Отправляем результаты сканирования обратно в мастер
          type - тип отправляемого отчета о сканировании (по умолчанию default)
          """
        levelId = component.get("id", -1)

        logging.info(f"Scanner -> Glenda: send result for component {levelId}")
        logging.debug(data)

        report = {
            "success": True,
            "level": level, # TODO: change
            "levelId": levelId,
            "type": "report", #TODO: убрать
            "result": {
                "type": type, # TODO: change
                "count": len(data),
                "data": data
            },
            "glenda": self.SCANNER_NAME,
        }

        report = json.dumps(report)

        self.producer.produce(self.REPORT_TOPIC, report.encode("utf-8"), callback=self.__kafka_callback)
        self.producer.flush()
