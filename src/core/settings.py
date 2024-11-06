class Settings:
    KAFKA_CONFIG = {
        'consumer': {
        'bootstrap_servers': ['localhost:9092'],
        'group_id': 'job_validator_group',
        'auto_offset_reset': 'earliest',
        'enable_auto_commit': False,  # Important for manual commits
        'max_poll_records': 100
        },
        'producer': {
            'bootstrap_servers': ['localhost:9092'],
            'acks': 'all'
        },
        'topics': {
            'raw_jobs': 'raw-jobs',
            'validated_jobs': 'validated-jobs',
            'failed_jobs': 'failed-jobs'
        }
    }
    KAFKA_BOOTSTRAP_SERVERS = ['localhost:9092']
    KAFKA_TOPICS = {
        'RAW_JOBS': 'raw-jobs',
        'VALIDATED_JOBS': 'validated-jobs',
        'NOTIFICATIONS': 'job-notifications'
    }
    EMAIL_CONFIG = {
        'SMTP_SERVER': 'smtp.gmail.com',
        'SMTP_PORT': 587
    }