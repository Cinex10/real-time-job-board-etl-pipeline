from abc import ABC, abstractmethod
from typing import List

from src.models.job_model import JobModel


class BaseNotificationService(ABC):
    def __init__(self, config):
        self.config = config
        
    @abstractmethod
    def setup(self):
        """Setup notifier with proper configuration"""
    
    @abstractmethod
    def format(self):
        """Logic for sending notifications"""
    
    @abstractmethod
    def notify(self, recipients: List[str]):
        """Logic for sending notifications"""
        
    @abstractmethod
    def add_to_digest(self, data: JobModel):
        """"""