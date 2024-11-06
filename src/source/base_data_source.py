from abc import ABC, abstractmethod
import json
from typing import List, Dict, Any
from datetime import datetime, timedelta
import pytz
from selenium.webdriver.chromium.webdriver import ChromiumDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.models.job_model import JobModel
from src.services.scraper import setup_driver
from src.services.logging import logger

tz = pytz.timezone('CET')

class BaseDataSource(ABC):
    """Base contract for all job sources"""
    
    def __init__(self, source_name: str):
        self.source_name = source_name
        self.base_url : str = None
        self.driver : ChromiumDriver = None
        self.waited_select_method = None
        self.waited_element_path = None
        self.timeout_in_s = 7
        self.last_fetch_time = datetime.now(tz) - timedelta(minutes=3)
        # self.last_fetch_time = datetime.fromtimestamp(1730857329, tz)

    def fetch_jobs(self) -> List[Dict[str, Any]]:
        """Fetch jobs from the source"""
        logger.info('Loading chrome driver to setup...')
        self.driver = setup_driver()
        logger.info('Chrome driver is ready')
        self.driver.get(self.base_url)
        try:
            WebDriverWait(self.driver, self.timeout_in_s, ignored_exceptions = []).until(EC.presence_of_element_located((self.waited_select_method, self.waited_element_path)))
            logger.info('Element found in web page')
            logs = self.driver.get_log('performance')
            raw_jobs = None
            for log in logs:
                log_entry = json.loads(log['message'])['message']
                if 'Network.responseReceived' == log_entry['method']:
                    params = log_entry['params']
                    if (('job_search_client' in params['response']['url']) and
                        (params['type'] == 'XHR') and
                        (params['response']['status'] == 200)):
                        requestId = params['requestId']
                        raw_jobs = self.driver.execute_cdp_cmd('Network.getResponseBody', {'requestId' : requestId})['body']
            raw_jobs = json.loads(raw_jobs)['results'][0]['hits']
            logger.info('Raw jobs loaded successfully')
            
            links = self.driver.find_elements('xpath', "//li[@data-testid='search-results-list-item-wrapper' and not(.//span[text()='Sponsorisé'])]//a[.//h4//div]")
                
            for link, job in zip(links, raw_jobs):
                job['link'] = link.get_attribute("href")
            # with open(f'{self.source_name}_{datetime.now()}_result.json', 'w') as json_file:
            #     json.dump(raw_jobs, json_file, indent=4)
            return raw_jobs
        except Exception as e:
            logger.error('Data source error ', e)
        finally:
            self.driver.quit()

    @abstractmethod
    def parse_job(self, raw_job: Dict[str, Any]) -> JobModel:
        """Parse raw job data into standardized format"""
    
    def ingest(self) -> List[JobModel]:
        raw_jobs = self.fetch_jobs()
        parsed_jobs : List[JobModel] = []
        for job in raw_jobs:
            job = self.parse_job(job)
            parsed_jobs.append(job)
        return parsed_jobs

    def update_fetch_time(self, job: JobModel):
            self.last_fetch_time = max(job.posted_date, self.last_fetch_time)
    
    def is_alreay_seen(self, job: JobModel) -> bool:
        """Check if the job is already fetched"""