import json
from typing import List
from kafka import KafkaConsumer, KafkaProducer
from src.core.settings import Settings
from src.models.job_model import JobModel
from src.services.base_notification_service import BaseNotificationService
from src.services.email_notification_service import EmailNotificationService
from src.services.logging import logger

smtp_config = {
    'server': 'smtp.gmail.com',
    'port': 587,
    'email': 'yaciniyac@gmail.com',
    'password': 'swxg tddu bozz svwo',
    'tls': True
}

class NotificationHandler:
    def __init__(self):
        self.consumer = KafkaConsumer(
            'validated-jobs',  # input topic
            bootstrap_servers= Settings.KAFKA_BOOTSTRAP_SERVERS,
            group_id='notification_group',
            auto_offset_reset='earliest',
            enable_auto_commit=False,
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )
    
    def notify(self, notifier: BaseNotificationService, data: List[JobModel], recipients: List[str]):
        for x in data:
            notifier.add_to_digest(x)
        notifier.format()
        notifier.notify(recipients)

    def process(self, recipients):
        """Main processing loop"""
        try:
            notifier = EmailNotificationService(smtp_config)
            for message in self.consumer:
                try:
                    logger.info(f'reading {type(message.value)} from raw-jobs topic')
                    job_data = [JobModel.model_validate_json(x) for x in message.value]
                    self.notify(notifier, job_data, recipients)
                    self.consumer.commit()

                except Exception as e:
                    logger.info(e)
                    logger.error(f"Error sending notification: {str(e)}")
                    continue

        except Exception as e:
            logger.error(f"Consumer error: {str(e)}")
            raise

    def close(self):
        """Close connections"""
        self.consumer.close()
        self.producer.close()