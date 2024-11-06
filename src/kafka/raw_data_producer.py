import json
from kafka import KafkaProducer
from src.core.settings import Settings
from src.source.base_data_source import BaseDataSource
from src.services.logging import logger

class RawDataProducer:
    def __init__(self, data_source: BaseDataSource):
        self.data_source = data_source
        self.producer = KafkaProducer(
            bootstrap_servers= Settings.KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        
    def produce(self):
        raw_data = self.data_source.ingest()
        new_jobs = []
        print(self.data_source.last_fetch_time)
        for data in raw_data:
            if not self.data_source.is_alreay_seen(data):
                new_jobs.append(data.model_dump_json())
                self.data_source.update_fetch_time(data)
        print(self.data_source.last_fetch_time)
        if (len(new_jobs) > 0):
            logger.info(f'{len(new_jobs)} new job offer ✅')
            logger.info('send raw_jobs ti kafka topic...')
            self.producer.send('raw-jobs', new_jobs)