from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
import smtplib
from typing import List
import jinja2
from src.models.job_model import JobModel
from src.services.base_notification_service import BaseNotificationService

logger = logging.getLogger(__name__)

class EmailNotificationService(BaseNotificationService):
    def __init__(self, config):
        super().__init__(config)
        self.template_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader('templates/')
        )
        self.job_buffer: List[JobModel] = []
    
    def setup(self):
        super().setup()

    def add_to_digest(self, job: JobModel):
        """Add job to digest buffer"""
        self.job_buffer.append(job)
    
    
    def format(self):
        template = self.template_env.get_template('job_notification_email_template.html')

        html_content = template.render(
                jobs=self.job_buffer,
                today_date= datetime.now().strftime('%B %d, %Y'),
                unsubscribe_url="http://example.com/unsubscribe"  # Replace with actual URL
            )
        return html_content
    
    def notify(self, recipients):
        try:
            html_content = self.format()        
            subject = f"Job Opportunities Digest - {len(self.job_buffer)} New Matches"
            msg = MIMEMultipart()
            msg['Subject'] = subject
            msg['From'] = self.config['email']
            msg['To'] = ', '.join(recipients)
            msg.attach(MIMEText(html_content, 'html'))
            
            with smtplib.SMTP(self.config['server'], self.config['port']) as server:
                server.starttls()
                server.login(self.config['email'], self.config['password'])
                server.send_message(msg)
            
            logger.info(f"Digest email sent with {len(self.job_buffer)} jobs")
            self.job_buffer.clear()
       
        except Exception as e:
            logger.error(f"Failed to send digest email: {str(e)}")
            raise