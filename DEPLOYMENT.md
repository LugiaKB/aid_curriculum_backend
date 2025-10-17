# Deployment Guide

This guide covers different deployment options for the AI Resume Builder API.

## Table of Contents
- [Local Development](#local-development)
- [Docker Deployment](#docker-deployment)
- [Production Deployment](#production-deployment)

---

## Local Development

### Prerequisites
- Python 3.8 or higher
- pip

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/LugiaKB/aid_curriculum_backend.git
   cd aid_curriculum_backend
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your configuration
   ```

5. **Run the server**
   ```bash
   python main.py
   ```
   
   Or use the helper script:
   ```bash
   ./run_server.sh
   ```

6. **Access the API**
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs

---

## Docker Deployment

### Prerequisites
- Docker
- Docker Compose (optional)

### Using Docker

1. **Build the Docker image**
   ```bash
   docker build -t ai-resume-builder .
   ```

2. **Run the container**
   ```bash
   docker run -p 8000:8000 --env-file .env ai-resume-builder
   ```

### Using Docker Compose

1. **Start the services**
   ```bash
   docker-compose up -d
   ```

2. **View logs**
   ```bash
   docker-compose logs -f
   ```

3. **Stop the services**
   ```bash
   docker-compose down
   ```

---

## Production Deployment

### Environment Configuration

For production, update your `.env` file with:

```env
OPENAI_API_KEY=your_production_api_key
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=False
```

### Security Considerations

1. **CORS Configuration**: Update CORS settings in `main.py` to restrict allowed origins:
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["https://yourdomain.com"],
       allow_credentials=True,
       allow_methods=["GET", "POST", "PUT", "DELETE"],
       allow_headers=["*"],
   )
   ```

2. **API Authentication**: Add authentication middleware (OAuth2, JWT, etc.)

3. **Rate Limiting**: Implement rate limiting to prevent abuse

4. **HTTPS**: Always use HTTPS in production

5. **Environment Variables**: Never commit `.env` files to version control

### Deployment Options

#### Option 1: Cloud Platform (Heroku, AWS, GCP, Azure)

**AWS EC2 Example:**

1. Launch an EC2 instance
2. Install Python and dependencies
3. Clone the repository
4. Set up environment variables
5. Use systemd or supervisor to keep the service running
6. Configure nginx as a reverse proxy
7. Set up SSL with Let's Encrypt

**Heroku Example:**

1. Create a `Procfile`:
   ```
   web: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

2. Deploy:
   ```bash
   heroku create your-app-name
   git push heroku main
   heroku config:set OPENAI_API_KEY=your_key
   ```

#### Option 2: Kubernetes

1. Create Kubernetes manifests
2. Deploy to your cluster:
   ```bash
   kubectl apply -f k8s/
   ```

#### Option 3: Serverless (AWS Lambda, Google Cloud Functions)

Use frameworks like Mangum to adapt FastAPI for serverless:

```python
from mangum import Mangum
handler = Mangum(app)
```

### Using a Process Manager

For production deployments, use a process manager like systemd or supervisor.

**systemd service example** (`/etc/systemd/system/resume-api.service`):

```ini
[Unit]
Description=AI Resume Builder API
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/aid_curriculum_backend
Environment="PATH=/path/to/venv/bin"
EnvironmentFile=/path/to/.env
ExecStart=/path/to/venv/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable resume-api
sudo systemctl start resume-api
```

### Nginx Configuration

**Example nginx config** (`/etc/nginx/sites-available/resume-api`):

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Database Integration

The current implementation uses in-memory storage. For production:

1. **Choose a database**: PostgreSQL, MongoDB, etc.
2. **Install database driver**: 
   ```bash
   pip install sqlalchemy psycopg2-binary
   ```
3. **Update models** to use actual database instead of in-memory storage
4. **Add database migrations** using Alembic

### Monitoring and Logging

1. **Application Logging**: Configure structured logging
   ```python
   import logging
   logging.basicConfig(level=logging.INFO)
   ```

2. **Monitoring**: Use tools like:
   - Prometheus + Grafana
   - DataDog
   - New Relic
   - CloudWatch (AWS)

3. **Error Tracking**: Integrate Sentry or similar:
   ```python
   import sentry_sdk
   sentry_sdk.init(dsn="your-sentry-dsn")
   ```

### Performance Optimization

1. **Add caching**: Use Redis for caching responses
2. **Connection pooling**: For database connections
3. **Load balancing**: Use multiple instances behind a load balancer
4. **CDN**: For static assets

### Backup Strategy

1. Regular database backups
2. Version control for code
3. Document restoration procedures

---

## Testing Deployment

### Run Tests

```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/
```

### Load Testing

Use tools like Apache Bench or Locust to test under load:

```bash
# Simple load test with ab
ab -n 1000 -c 10 http://localhost:8000/health
```

---

## Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Find process using port 8000
   lsof -i :8000
   # Kill the process
   kill -9 <PID>
   ```

2. **Module not found errors**
   ```bash
   # Ensure virtual environment is activated
   # Reinstall dependencies
   pip install -r requirements.txt
   ```

3. **OpenAI API errors**
   - Verify API key is correct
   - Check API quota and limits
   - System falls back to templates if API fails

---

## Maintenance

### Updating Dependencies

```bash
# Update all packages
pip install --upgrade -r requirements.txt

# Or update specific package
pip install --upgrade fastapi
```

### Monitoring Logs

```bash
# For systemd
sudo journalctl -u resume-api -f

# For Docker
docker-compose logs -f
```

---

## Support

For issues and questions:
- Check the API documentation at `/docs`
- Review the README.md
- Open an issue on GitHub
