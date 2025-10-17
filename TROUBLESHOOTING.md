# Troubleshooting Guide

Common issues and their solutions for the AI Resume Builder API.

## Table of Contents
- [Installation Issues](#installation-issues)
- [Runtime Issues](#runtime-issues)
- [API Issues](#api-issues)
- [AI Service Issues](#ai-service-issues)
- [Performance Issues](#performance-issues)

---

## Installation Issues

### Issue: `pip install` fails with timeout errors

**Symptoms:**
```
ReadTimeoutError: HTTPSConnectionPool(host='pypi.org', port=443): Read timed out.
```

**Solutions:**
1. Increase pip timeout:
   ```bash
   pip install -r requirements.txt --timeout 100
   ```

2. Use a different PyPI mirror:
   ```bash
   pip install -r requirements.txt --index-url https://pypi.org/simple
   ```

3. Install packages one at a time:
   ```bash
   pip install fastapi uvicorn pydantic pydantic-settings python-dotenv openai
   ```

### Issue: Module not found after installation

**Symptoms:**
```
ModuleNotFoundError: No module named 'fastapi'
```

**Solutions:**
1. Ensure virtual environment is activated:
   ```bash
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate      # Windows
   ```

2. Verify Python version:
   ```bash
   python --version  # Should be 3.8+
   ```

3. Reinstall in the correct environment:
   ```bash
   pip install -r requirements.txt
   ```

### Issue: Permission denied during installation

**Symptoms:**
```
ERROR: Could not install packages due to an EnvironmentError: [Errno 13] Permission denied
```

**Solutions:**
1. Use virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Install for user only:
   ```bash
   pip install -r requirements.txt --user
   ```

---

## Runtime Issues

### Issue: Port 8000 already in use

**Symptoms:**
```
ERROR:    [Errno 48] Address already in use
```

**Solutions:**
1. Find and kill the process:
   ```bash
   # Linux/Mac
   lsof -ti:8000 | xargs kill -9
   
   # Windows
   netstat -ano | findstr :8000
   taskkill /PID <PID> /F
   ```

2. Use a different port:
   ```bash
   # Edit .env
   API_PORT=8001
   
   # Or run directly
   uvicorn main:app --port 8001
   ```

### Issue: Server starts but can't access from browser

**Symptoms:**
- Server logs show no errors
- Browser shows "Can't connect" or timeout

**Solutions:**
1. Check if server is listening:
   ```bash
   curl http://localhost:8000/health
   ```

2. Verify host configuration:
   ```bash
   # In .env
   API_HOST=0.0.0.0  # Not 127.0.0.1 if accessing from network
   ```

3. Check firewall settings:
   ```bash
   # Allow port 8000
   sudo ufw allow 8000
   ```

### Issue: Import errors when starting server

**Symptoms:**
```
ImportError: cannot import name 'BaseSettings' from 'pydantic'
```

**Solutions:**
1. Verify correct pydantic version:
   ```bash
   pip show pydantic  # Should be 2.5.0+
   ```

2. Update pydantic:
   ```bash
   pip install --upgrade pydantic pydantic-settings
   ```

3. Clear Python cache:
   ```bash
   find . -type d -name __pycache__ -exec rm -r {} +
   find . -type f -name "*.pyc" -delete
   ```

---

## API Issues

### Issue: 422 Validation Error on requests

**Symptoms:**
```json
{
  "detail": [
    {
      "loc": ["body", "contact", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

**Solutions:**
1. Check request format matches schema:
   ```bash
   # View schema in docs
   curl http://localhost:8000/docs
   ```

2. Ensure required fields are included:
   ```json
   {
     "full_name": "Required",
     "contact": {
       "email": "required@example.com"
     }
   }
   ```

3. Verify content-type header:
   ```bash
   curl -H "Content-Type: application/json" ...
   ```

### Issue: CORS errors in browser

**Symptoms:**
```
Access to fetch at 'http://localhost:8000/api/resumes' from origin 'http://localhost:3000' 
has been blocked by CORS policy
```

**Solutions:**
1. Update CORS configuration in `main.py`:
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["http://localhost:3000"],  # Add your frontend URL
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

2. For development, allow all origins (not for production):
   ```python
   allow_origins=["*"]
   ```

### Issue: 404 Not Found for existing endpoints

**Symptoms:**
```
{"detail": "Not Found"}
```

**Solutions:**
1. Check URL path (including /api prefix):
   ```bash
   # Correct
   curl http://localhost:8000/api/resumes/
   
   # Incorrect
   curl http://localhost:8000/resumes/
   ```

2. Verify router is registered:
   ```python
   # In main.py
   app.include_router(resumes_router)
   ```

3. Check trailing slashes:
   ```bash
   # Some endpoints may require trailing slash
   /api/resumes/  vs  /api/resumes
   ```

---

## AI Service Issues

### Issue: AI generation returns template-based content only

**Symptoms:**
- Always getting generic responses
- No personalized content

**Solutions:**
1. Check if OpenAI API key is set:
   ```bash
   # In .env
   OPENAI_API_KEY=sk-...
   ```

2. Verify API key is loaded:
   ```python
   from app.config import settings
   print(settings.openai_api_key)  # Should not be None
   ```

3. Test API key separately:
   ```bash
   curl https://api.openai.com/v1/models \
     -H "Authorization: Bearer $OPENAI_API_KEY"
   ```

### Issue: OpenAI API errors

**Symptoms:**
```
Error generating resume content: Rate limit exceeded
```

**Solutions:**
1. Check API quota:
   - Visit OpenAI dashboard
   - Verify billing and usage limits

2. Implement retry logic:
   ```python
   # Add exponential backoff
   from tenacity import retry, wait_exponential
   ```

3. Use lower tier model:
   ```python
   # In ai_service.py
   model="gpt-3.5-turbo"  # Instead of gpt-4
   ```

### Issue: Slow AI responses

**Symptoms:**
- Requests taking >30 seconds
- Timeout errors

**Solutions:**
1. Reduce max_tokens:
   ```python
   max_tokens=800  # Instead of 1500
   ```

2. Use streaming (for future implementation):
   ```python
   stream=True
   ```

3. Add timeout to OpenAI calls:
   ```python
   response = client.chat.completions.create(
       ...,
       timeout=30
   )
   ```

---

## Performance Issues

### Issue: High memory usage

**Symptoms:**
- Server using excessive RAM
- Out of memory errors

**Solutions:**
1. Clear in-memory storage periodically:
   ```python
   # Add endpoint to clear old resumes
   resume_model._storage.clear()
   ```

2. Implement LRU cache:
   ```python
   from functools import lru_cache
   
   @lru_cache(maxsize=100)
   def cached_function():
       pass
   ```

3. Use database instead of in-memory storage

### Issue: Slow response times

**Symptoms:**
- API responses taking >5 seconds
- High latency

**Solutions:**
1. Enable caching:
   ```python
   # Cache AI responses
   from functools import lru_cache
   ```

2. Profile the code:
   ```bash
   pip install py-spy
   py-spy top -- python main.py
   ```

3. Use async operations:
   ```python
   async def process_resume():
       # Use async/await
       pass
   ```

4. Add database indexes (when using database)

### Issue: Connection timeouts

**Symptoms:**
```
TimeoutError: Server took too long to respond
```

**Solutions:**
1. Increase client timeout:
   ```python
   import httpx
   client = httpx.Client(timeout=60.0)
   ```

2. Optimize AI requests:
   ```python
   # Reduce response length
   max_tokens=500
   ```

3. Implement request queuing for heavy operations

---

## Docker Issues

### Issue: Docker build fails

**Symptoms:**
```
ERROR: failed to solve: process "/bin/sh -c pip install -r requirements.txt" did not complete
```

**Solutions:**
1. Check Dockerfile syntax
2. Increase Docker memory:
   ```bash
   # Docker Desktop → Settings → Resources
   Memory: 4GB or more
   ```

3. Clear Docker cache:
   ```bash
   docker system prune -a
   ```

### Issue: Container exits immediately

**Symptoms:**
```
Container exited with code 1
```

**Solutions:**
1. Check container logs:
   ```bash
   docker logs <container-id>
   ```

2. Run interactively:
   ```bash
   docker run -it ai-resume-builder bash
   ```

3. Check environment variables:
   ```bash
   docker run --env-file .env ...
   ```

---

## Testing Issues

### Issue: Tests fail with import errors

**Symptoms:**
```
ModuleNotFoundError: No module named 'app'
```

**Solutions:**
1. Run from project root:
   ```bash
   cd /path/to/aid_curriculum_backend
   pytest tests/
   ```

2. Add to PYTHONPATH:
   ```bash
   export PYTHONPATH="${PYTHONPATH}:$(pwd)"
   pytest tests/
   ```

3. Install in editable mode:
   ```bash
   pip install -e .
   ```

---

## Getting More Help

### Enable Debug Logging

Add to `.env`:
```
DEBUG=True
```

Add to code:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Logs

```bash
# View server logs
tail -f /var/log/resume-api.log

# Docker logs
docker-compose logs -f
```

### Collect System Information

```bash
python --version
pip list
uname -a  # Linux/Mac
systeminfo  # Windows
```

### Report Issues

When reporting issues on GitHub, include:
1. Python version
2. Operating system
3. Full error message
4. Steps to reproduce
5. Expected vs actual behavior
6. Relevant logs

---

## Still Having Issues?

- Check the [GitHub Issues](https://github.com/LugiaKB/aid_curriculum_backend/issues)
- Review the [API Documentation](API_DOCS.md)
- Read the [Architecture Overview](ARCHITECTURE.md)
- Open a new issue with details

Remember: The API works without an OpenAI key using template-based generation!
