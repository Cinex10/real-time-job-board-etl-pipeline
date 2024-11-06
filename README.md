# Job Board Pipeline

An automated job scraping and notification system powered by Apache Kafka. Fetches job listings asynchronously, processes them through a streaming pipeline, and sends customized email digests based on user preferences.

## 🚀 Features

- **Streaming Architecture**: Real-time job processing using Apache Kafka
- **Async Job Fetching**: Efficiently fetches jobs from source
- **Email Notifications**: 
  - Daily digest of matching jobs
  - Responsive HTML email templates
  - Support for multiple email providers
- **Fault Tolerance**: Built-in message persistence and retry mechanisms

## 🛠️ Tech Stack

- Python 3.9+
- Apache Kafka
- kafka-python
- pydantic
- Jinja2

## 📋 Prerequisites

- Docker Engine 20.10+
- Docker Compose V2
- Git

## ⚙️ Configuration

1. **Kafka Settings** (.env file):
```env
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_TOPIC=job_listings
KAFKA_GROUP_ID=job_processor

SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_EMAIL=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

## 🚀 Quick Start

1. Clone the repository:
```bash
git clone https://github.com/yourusername/job-board-pipeline.git
cd job-board-pipeline
```

2. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your settings
```

3. Start the services:
```bash
docker compose up -d
```

4. Check services status:
```bash
docker compose ps
```

## ⚙️ Configuration

1. **Environment Variables** (.env):
```env
# Kafka
KAFKA_BOOTSTRAP_SERVERS=kafka:9092
KAFKA_TOPIC=job_listings
KAFKA_GROUP_ID=job_processor

# SMTP
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_EMAIL=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Job Source
API_URL=your-job-api-url
API_KEY=your-api-key

# Schedule
SCHEDULE_START_HOUR=8
SCHEDULE_END_HOUR=1
SCHEDULE_INTERVAL_MINUTES=5

# Notification
NOTIFICATION_EMAILS=email1@example.com,email2@example.com
```

2. **Job Matching Criteria** (config/criteria.json):
```json
{
  "title_keywords": ["python", "data engineer"],
  "required_skills": ["python", "sql"],
  "locations": ["remote", "new york"]
}
```

## 🐳 Docker Commands

Start services:
```bash
# Start all services
docker compose up -d

# Start specific service
docker compose up -d pipeline

# View logs
docker compose logs -f pipeline

# Stop services
docker compose down

# Rebuild after changes
docker compose build pipeline
docker compose up -d pipeline
```

Check Kafka:
```bash
# List topics
docker compose exec kafka kafka-topics --list --bootstrap-server localhost:9092

# Create topic manually if needed
docker compose exec kafka kafka-topics \
    --create \
    --bootstrap-server localhost:9092 \
    --replication-factor 1 \
    --partitions 3 \
    --topic job_listings
```

## 📊 Monitoring

View logs:
```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f pipeline
docker compose logs -f kafka
```

Check containers:
```bash
# List containers
docker compose ps

# Container stats
docker stats
```

## 🐛 Troubleshooting

1. **Kafka Connection Issues**:
```bash
# Check Kafka is running
docker compose ps kafka

# Check Kafka logs
docker compose logs kafka

# Verify topic
docker compose exec kafka kafka-topics \
    --describe \
    --bootstrap-server localhost:9092 \
    --topic job_listings
```

2. **Pipeline Issues**:
```bash
# Check pipeline logs
docker compose logs pipeline

# Restart pipeline
docker compose restart pipeline

# Check environment variables
docker compose config
```

## 🔄 Development

1. Local development with Docker:
```bash
# Build with development configuration
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d

# Hot reload for code changes
docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build pipeline
```

2. Update dependencies:
```bash
# Update requirements.txt
pip freeze > docker/requirements.txt

# Rebuild container
docker compose build pipeline
```

## 📝 Maintenance

Backup data:
```bash
# Create backup directory
mkdir -p backups

# Backup Kafka topics
docker compose exec kafka kafka-topics \
    --describe \
    --bootstrap-server localhost:9092 \
    > backups/topics_$(date +%Y%m%d).txt
```

Clean up:
```bash
# Remove unused containers
docker compose down

# Remove volumes
docker compose down -v

# Clean all
docker compose down -v --rmi all --remove-orphans
```

## 🔒 Security Notes

1. Always use `.env` for sensitive data
2. Never commit `.env` to repository
3. Use secrets management in production
4. Regularly update dependencies
5. Monitor container logs for suspicious activity

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## 📝 License

[MIT](https://choosealicense.com/licenses/mit/)

---
*Built with Docker for easy deployment and scalability.*