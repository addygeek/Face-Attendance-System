# Deployment Requirements - Face Attendance System

## Python 3.11+ Deployment Guide

**Last Updated**: November 26, 2025
**Python Version**: 3.11+
**Status**: Production Ready

---

## 📋 Complete Requirements

### Core Dependencies (Required)

| Package | Version | Purpose | Size |
|---------|---------|---------|------|
| numpy | >=1.23.0,<2.0.0 | Numerical computing | ~25 MB |
| opencv-python | >=4.8.0 | Image processing | ~90 MB |
| flask | >=2.3.0 | Web framework | ~2 MB |
| flask-cors | >=4.0.0 | CORS support | ~1 MB |
| mediapipe | >=0.10.0 | Face detection | ~150 MB |

**Total Size**: ~270 MB

### Optional Dependencies

| Package | Version | Purpose | When to Use |
|---------|---------|---------|------------|
| pytest | >=7.0.0 | Testing | Development |
| pytest-cov | >=4.0.0 | Test coverage | Development |
| gunicorn | >=21.0.0 | Production server | Production |
| python-dotenv | >=1.0.0 | Environment variables | Production |
| flask-sqlalchemy | >=3.0.0 | Database ORM | Future use |
| sqlalchemy | >=2.0.0 | Database toolkit | Future use |

---

## 🚀 Installation Methods

### Method 1: Direct pip Installation (Recommended)

#### Windows
```powershell
# 1. Install Python 3.11
# Download from: https://www.python.org/downloads/
# Check "Add Python to PATH" during installation

# 2. Create virtual environment
python -m venv .venv

# 3. Activate virtual environment
.venv\Scripts\activate

# 4. Upgrade pip
python -m pip install --upgrade pip

# 5. Install requirements
pip install -r ml_model/requirements.txt

# 6. Verify installation
python -c "import cv2; import mediapipe; import flask; print('✓ All installed')"
```

#### Mac
```bash
# 1. Install Python 3.11 via Homebrew
brew install python@3.11

# 2. Create virtual environment
python3.11 -m venv .venv

# 3. Activate virtual environment
source .venv/bin/activate

# 4. Upgrade pip
python3 -m pip install --upgrade pip

# 5. Install requirements
pip install -r ml_model/requirements.txt

# 6. Verify installation
python3 -c "import cv2; import mediapipe; import flask; print('✓ All installed')"
```

#### Linux (Ubuntu/Debian)
```bash
# 1. Install Python 3.11
sudo apt-get update
sudo apt-get install python3.11 python3.11-venv python3.11-dev

# 2. Create virtual environment
python3.11 -m venv .venv

# 3. Activate virtual environment
source .venv/bin/activate

# 4. Upgrade pip
python3 -m pip install --upgrade pip

# 5. Install system dependencies (for OpenCV)
sudo apt-get install libsm6 libxext6 libxrender-dev

# 6. Install requirements
pip install -r ml_model/requirements.txt

# 7. Verify installation
python3 -c "import cv2; import mediapipe; import flask; print('✓ All installed')"
```

---

### Method 2: Conda Installation (Alternative)

```bash
# 1. Install Conda
# Download from: https://www.anaconda.com/download

# 2. Create environment
conda create -n face-attendance python=3.11

# 3. Activate environment
conda activate face-attendance

# 4. Install dependencies
conda install numpy opencv flask flask-cors mediapipe

# 5. Verify installation
python -c "import cv2; import mediapipe; import flask; print('✓ All installed')"
```

---

### Method 3: Docker Deployment

#### Dockerfile
```dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY ml_model/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 5000

# Run application
CMD ["python", "ml_model/app.py"]
```

#### Build and Run
```bash
# Build image
docker build -t face-attendance:1.1 .

# Run container
docker run -p 5000:5000 face-attendance:1.1

# Run with volume mount
docker run -p 5000:5000 -v $(pwd)/data:/app/data face-attendance:1.1
```

---

### Method 4: Production Deployment with Gunicorn

```bash
# 1. Install gunicorn
pip install gunicorn

# 2. Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 ml_model.app:app

# 3. Or with configuration file
gunicorn -c gunicorn_config.py ml_model.app:app
```

#### gunicorn_config.py
```python
import multiprocessing

# Server socket
bind = "0.0.0.0:5000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Process naming
proc_name = "face-attendance"

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL
keyfile = None
certfile = None
ssl_version = 5
cert_reqs = 0
ca_certs = None
suppress_ragged_eof = True
```

---

## 🐳 Docker Compose Deployment

#### docker-compose.yml
```yaml
version: '3.8'

services:
  face-attendance:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./data:/app/data
      - ./web_app/embeddings:/app/web_app/embeddings
    environment:
      - FLASK_ENV=production
      - FLASK_DEBUG=0
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

#### Run with Docker Compose
```bash
# Start
docker-compose up -d

# Stop
docker-compose down

# View logs
docker-compose logs -f
```

---

## 🔧 System Requirements

### Minimum Requirements
- **CPU**: 2 cores
- **RAM**: 2 GB
- **Disk**: 500 MB (+ data storage)
- **Python**: 3.11+
- **OS**: Windows, Mac, or Linux

### Recommended Requirements
- **CPU**: 4+ cores
- **RAM**: 4+ GB
- **Disk**: 1 GB (+ data storage)
- **Python**: 3.11+
- **OS**: Linux (for production)

### Network Requirements
- **Port**: 5000 (Flask default)
- **Bandwidth**: 1 Mbps minimum
- **Internet**: Required for first-time setup

---

## 📦 Dependency Details

### numpy (>=1.23.0,<2.0.0)
- **Purpose**: Numerical computing for embeddings
- **Size**: ~25 MB
- **Python 3.11**: ✅ Fully supported
- **Installation**: `pip install numpy`

### opencv-python (>=4.8.0)
- **Purpose**: Image processing and face detection
- **Size**: ~90 MB
- **Python 3.11**: ✅ Fully supported
- **Installation**: `pip install opencv-python`
- **Note**: Requires system libraries on Linux

### flask (>=2.3.0)
- **Purpose**: Web framework for REST API
- **Size**: ~2 MB
- **Python 3.11**: ✅ Fully supported
- **Installation**: `pip install flask`

### flask-cors (>=4.0.0)
- **Purpose**: Cross-Origin Resource Sharing support
- **Size**: ~1 MB
- **Python 3.11**: ✅ Fully supported
- **Installation**: `pip install flask-cors`

### mediapipe (>=0.10.0)
- **Purpose**: Face detection and landmark extraction
- **Size**: ~150 MB
- **Python 3.11**: ✅ Fully supported
- **Installation**: `pip install --no-cache-dir mediapipe`
- **Note**: May require internet connection for first-time setup

---

## ✅ Verification Checklist

After installation, verify everything works:

```bash
# 1. Check Python version
python --version
# Should show: Python 3.11.x

# 2. Check pip version
pip --version
# Should show: pip 24.x.x

# 3. Check virtual environment
which python  # Mac/Linux
where python  # Windows
# Should show path to .venv

# 4. Check individual packages
python -c "import numpy; print(f'numpy {numpy.__version__}')"
python -c "import cv2; print(f'opencv {cv2.__version__}')"
python -c "import flask; print(f'flask {flask.__version__}')"
python -c "import flask_cors; print('flask-cors OK')"
python -c "import mediapipe; print('mediapipe OK')"

# 5. Run all checks
python -c "
import numpy
import cv2
import flask
import flask_cors
import mediapipe
print('✓ All dependencies installed successfully!')
"
```

---

## 🚀 Quick Deployment

### Windows (5 minutes)
```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r ml_model/requirements.txt
cd ml_model
python app.py
```

### Mac (5 minutes)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r ml_model/requirements.txt
cd ml_model
python3 app.py
```

### Linux (5 minutes)
```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r ml_model/requirements.txt
cd ml_model
python3 app.py
```

### Docker (2 minutes)
```bash
docker build -t face-attendance .
docker run -p 5000:5000 face-attendance
```

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'cv2'"
```bash
pip install opencv-python
```

### Issue: "ModuleNotFoundError: No module named 'mediapipe'"
```bash
pip install --no-cache-dir mediapipe
# Or use Conda
conda install mediapipe
```

### Issue: "Port 5000 already in use"
```bash
# Windows
netstat -ano | findstr :5000

# Mac/Linux
lsof -i :5000

# Kill process or use different port
```

### Issue: "Permission denied" on Linux
```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Or use sudo
sudo docker run -p 5000:5000 face-attendance
```

### Issue: "Mediapipe installation fails"
```bash
# Try without cache
pip install --no-cache-dir mediapipe

# Or use Conda
conda install mediapipe

# Or use pre-built wheel
pip install mediapipe-0.10.0-cp311-cp311-win_amd64.whl
```

---

## 📊 Deployment Checklist

- [ ] Python 3.11+ installed
- [ ] Virtual environment created
- [ ] All dependencies installed
- [ ] Verification checks passed
- [ ] Backend starts without errors
- [ ] Web interface loads
- [ ] Camera access working
- [ ] Faces detected in real-time
- [ ] Attendance logged correctly
- [ ] API endpoints responding

---

## 🔐 Production Deployment

### Security Considerations
1. Use HTTPS (SSL/TLS)
2. Set Flask DEBUG=False
3. Use strong SECRET_KEY
4. Implement authentication
5. Use firewall rules
6. Regular backups
7. Monitor logs

### Performance Optimization
1. Use Gunicorn with multiple workers
2. Enable caching
3. Use CDN for static files
4. Implement rate limiting
5. Monitor resource usage
6. Scale horizontally if needed

### Monitoring
1. Set up logging
2. Monitor CPU/RAM usage
3. Track API response times
4. Monitor error rates
5. Set up alerts

---

## 📚 Additional Resources

- **Python 3.11 Docs**: https://docs.python.org/3.11/
- **Flask Docs**: https://flask.palletsprojects.com/
- **OpenCV Docs**: https://docs.opencv.org/
- **MediaPipe Docs**: https://google.github.io/mediapipe/
- **Docker Docs**: https://docs.docker.com/

---

## 🎯 Summary

The Face Attendance System is fully compatible with Python 3.11+ and can be deployed easily using:

✅ Direct pip installation
✅ Conda environment
✅ Docker containers
✅ Production servers (Gunicorn)
✅ Cloud platforms

All dependencies are listed in `requirements.txt` and are production-ready.

**Ready for deployment!** 🚀

