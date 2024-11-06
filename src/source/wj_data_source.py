from datetime import datetime
from typing import Any, Dict
import pytz
from src.core.singleton import singleton
from src.models.job_model import JobModel
from selenium.webdriver.common.by import By
from src.source.base_data_source import BaseDataSource

tz = pytz.timezone('CET')

@singleton
class WelcomeToTheJungleDataSource(BaseDataSource):
    def __init__(self):
        super().__init__("welcome-to-the-jungle")
        self.base_url = "https://www.welcometothejungle.com/fr/jobs?refinementList%5Bcontract_type%5D%5B%5D=internship&page=1&query=data&aroundQuery=worldwide&sortBy=mostRecent"
        self.waited_select_method = By.XPATH
        self.waited_element_path = '//*[@id="app"]/div/div/div/div[2]/div/ul'
        
    def parse_job(self, raw_job: Dict[str, Any]) -> JobModel:
        company_name = raw_job['organization']['name']
        job_title = raw_job['name']
        link = raw_job['link']
        office = raw_job['offices'][0]
        state = office['state']
        city = office['city']
        country = office['country']
        model = JobModel(
            job_id= str(hash((company_name, job_title))),
            company= company_name,
            posted_date= datetime.fromtimestamp(raw_job['published_at_timestamp'] , tz),
            title= job_title,
            source= self.source_name,
            fetched_date= datetime.now(tz),
            state= state,
            city= city,
            country= country,
            link= link
            )
        return model
    
    def is_alreay_seen(self, job: JobModel) -> bool:
        return job.posted_date <= self.last_fetch_time