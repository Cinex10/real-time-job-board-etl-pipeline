import logging
import time
import os
import sys
import threading


logger = logging.getLogger(__name__)

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



from src.kafka.job_validator_handler import JobValidatorHandler
from src.kafka.raw_data_producer import RawDataProducer
from src.source.wj_data_source import WelcomeToTheJungleDataSource
from src.kafka.notification_handler import NotificationHandler

def run_producer(producer : RawDataProducer, stop_event):
    while not stop_event.is_set():
        try:
            producer.produce()
        except Exception as e:
            logger.error(f"Producer error: {e}")
        time.sleep(60 * 10)

def run_validator(validator: JobValidatorHandler, stop_event):
    while not stop_event.is_set():
        try:
            validator.process()
        except Exception as e:
            logger.error(f"Validator error: {e}")

def run_notifier(notifier: NotificationHandler, stop_event):
    while not stop_event.is_set():
        try:
            recipients = ['y.driss@esi-sba.dz']
            notifier.process(recipients)
        except Exception as e:
            logger.error(f"Notifier error: {e}")

def main():
    data_source = WelcomeToTheJungleDataSource()
    
    producer = RawDataProducer(data_source)
    validator = JobValidatorHandler()
    notifier = NotificationHandler()
    
    # Setup stop event for graceful shutdown
    stop_event = threading.Event()
    
    try:
        # Create threads for each component
        threads = [
            threading.Thread(target=run_producer, args=(producer, stop_event)),
            threading.Thread(target=run_validator, args=(validator, stop_event)),
            threading.Thread(target=run_notifier, args=(notifier, stop_event)),
        ]
        
        # Start all threads
        for thread in threads:
            thread.start()
            
        logger.info("Pipeline started successfully")
        
        # Keep main thread running
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("Shutting down pipeline...")
        stop_event.set()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
            
        logger.info("Pipeline shutdown complete")

if __name__ == "__main__":
    main()