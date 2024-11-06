import json
from typing import List
from kafka import KafkaConsumer, KafkaProducer
from src.core.settings import Settings
from src.models.job_model import JobModel
from src.services.logging import logger

class JobValidatorHandler:
    def __init__(self):
        self.consumer = KafkaConsumer(
            'raw-jobs',  # input topic
            bootstrap_servers= Settings.KAFKA_BOOTSTRAP_SERVERS,
            group_id='job_validator_group',
            auto_offset_reset='earliest',
            enable_auto_commit=False,
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )
        self.producer = KafkaProducer(
            bootstrap_servers= Settings.KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        

    def validate_job(self, raw_jobs: List[JobModel]) -> bool:
        """Simple validation of job data"""
        logger.info(f'validating job data...')
        return True

    def process(self):
        """Main processing loop"""
        try:
            # Get messages from consumer
            for message in self.consumer:
                try:
                    # logger.info(f'reading {type(message.value)} from raw-jobs topic')
                    # Get the job data
                    job_data = [JobModel.model_validate_json(x) for x in message.value]
                    # Validate the job
                    if self.validate_job(job_data):
                        # Add timestamp
                        # job_data['validation_date'] = datetime.now().isoformat()
                        
                        # Send to validated jobs topic
                        job_data = [x.model_dump_json() for x in job_data]
                        self.producer.send('validated-jobs', job_data)
                        logger.info(f"Validated jobs")
                    else:
                    #     # Send to failed jobs topic
                    #     self.producer.send('failed-jobs', {
                    #         'job': job_data,
                    #         'error': 'Missing required fields',
                    #         'timestamp': datetime.now().isoformat()
                    #     })
                        logger.warning(f"Invalid job data: {job_data}")

                    # Commit the offset after processing
                    self.consumer.commit()

                except Exception as e:
                    logger.info(e)
                    logger.error(f"Error processing message: {str(e)}")
                    continue

        except Exception as e:
            logger.error(f"Consumer error: {str(e)}")
            raise

    def close(self):
        """Close connections"""
        self.consumer.close()
        self.producer.close()