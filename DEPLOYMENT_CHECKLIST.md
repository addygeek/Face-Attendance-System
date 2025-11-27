# Deployment Checklist - Face Attendance System v1.1

## Pre-Deployment Verification

### System Requirements
- [ ] Python 3.11+ installed
- [ ] 2GB RAM minimum available
- [ ] 500MB disk space available
- [ ] Internet connection for first-time setup
- [ ] Webcam available (for testing)

### Python Environment
- [ ] Python version verified: `python --version`
- [ ] Pip version verified: `pip --version`
- [ ] Virtual environment created
- [ ] Virtual environment activated
- [ ] Pip upgraded: `python -m pip install --upgrade pip`

### Dependencies Installation
- [ ] `numpy>=1.23.0,<2.0.0` installed
- [ ] `opencv-python>=4.8.0` installed
- [ ] `flask>=2.3.0` installed
- [ ] `flask-cors>=4.0.0` installed
- [ ] `mediapipe>=0.10.0` installed
- [ ] All dependencies verified: `python verify_installation.py`

### Project Structure
- [ ] `ml_model/` directory exists
- [ ] `web_app/` directory exists
- [ ] `data/` directory exists
- [ ] `ml_model/app.py` exists
- [ ] `ml_model/requirements.txt` exists
- [ ] `web_app/index.html` exists
- [ ] `web_app/script.js` exists
- [ ] `web_app/attendance.html` exists

### Configuration
- [ ] Flask DEBUG mode set to False (production)
- [ ] API port 5000 available
- [ ] CORS enabled for web access
- [ ] JSON storage directory writable
- [ ] Embeddings directory writable

---

## Installation Verification

### Run Verification Script
```bash
python verify_installation.py
```

Expected output:
```
✓ Python 3.11+ is compatible
✓ Pip is installed
✓ Running in virtual environment
✓ numpy installed
✓ opencv-python installed
✓ flask installed
✓ flask-cors installed
✓ mediapipe installed
✓ All dependencies are installed!
✓ System is ready for deployment!
```

### Manual Verification
```bash
# Check each package
python -c "import numpy; print(f'numpy {numpy.__version__}')"
python -c "import cv2; print(f'opencv {cv2.__version__}')"
python -c "import flask; print(f'flask {flask.__version__}')"
python -c "import flask_cors; print('flask-cors OK')"
python -c "import mediapipe; print('mediapipe OK')"
```

---

## Pre-Deployment Testing

### Backend Testing
- [ ] Backend starts without errors: `python ml_model/app.py`
- [ ] API responds to health check: `curl http://localhost:5000/health`
- [ ] No port conflicts
- [ ] No permission errors
- [ ] No missing module errors

### Frontend Testing
- [ ] `web_app/index.html` loads in browser
- [ ] `web_app/attendance.html` loads in browser
- [ ] `web_app/register.html` loads in browser
- [ ] Camera access requested and granted
- [ ] Video stream displays
- [ ] Face detection working
- [ ] Attendance logging working

### API Testing
- [ ] `POST /api/attendance` works
- [ ] `GET /api/attendance` works
- [ ] `GET /api/embeddings` works
- [ ] `GET /health` works
- [ ] Error handling works
- [ ] CORS headers present

### Data Storage Testing
- [ ] `data/attendance.json` created
- [ ] Records saved correctly
- [ ] Records retrieved correctly
- [ ] Filtering works
- [ ] Deletion works

---

## Deployment Methods

### Method 1: Direct Installation (Windows)
- [ ] Python 3.11 installed
- [ ] Virtual environment created: `python -m venv .venv`
- [ ] Virtual environment activated: `.venv\Scripts\activate`
- [ ] Dependencies installed: `pip install -r ml_model/requirements.txt`
- [ ] Verification passed: `python verify_installation.py`
- [ ] Backend starts: `python ml_model/app.py`

### Method 2: Direct Installation (Mac)
- [ ] Python 3.11 installed via Homebrew
- [ ] Virtual environment created: `python3 -m venv .venv`
- [ ] Virtual environment activated: `source .venv/bin/activate`
- [ ] Dependencies installed: `pip install -r ml_model/requirements.txt`
- [ ] Verification passed: `python3 verify_installation.py`
- [ ] Backend starts: `python3 ml_model/app.py`

### Method 3: Direct Installation (Linux)
- [ ] Python 3.11 installed: `sudo apt-get install python3.11`
- [ ] Virtual environment created: `python3.11 -m venv .venv`
- [ ] Virtual environment activated: `source .venv/bin/activate`
- [ ] System dependencies installed: `sudo apt-get install libsm6 libxext6 libxrender-dev`
- [ ] Dependencies installed: `pip install -r ml_model/requirements.txt`
- [ ] Verification passed: `python3 verify_installation.py`
- [ ] Backend starts: `python3 ml_model/app.py`

### Method 4: Conda Installation
- [ ] Conda installed
- [ ] Environment created: `conda create -n face-attendance python=3.11`
- [ ] Environment activated: `conda activate face-attendance`
- [ ] Dependencies installed: `conda install numpy opencv flask flask-cors mediapipe`
- [ ] Verification passed: `python verify_installation.py`
- [ ] Backend starts: `python ml_model/app.py`

### Method 5: Docker Deployment
- [ ] Docker installed
- [ ] Dockerfile created
- [ ] Image built: `docker build -t face-attendance:1.1 .`
- [ ] Container runs: `docker run -p 5000:5000 face-attendance:1.1`
- [ ] API responds: `curl http://localhost:5000/health`
- [ ] Web interface accessible: `http://localhost:5000`

### Method 6: Production Deployment (Gunicorn)
- [ ] Gunicorn installed: `pip install gunicorn`
- [ ] Gunicorn config created
- [ ] Gunicorn starts: `gunicorn -w 4 -b 0.0.0.0:5000 ml_model.app:app`
- [ ] Multiple workers running
- [ ] Load balancing working
- [ ] Graceful shutdown working

---

## Production Deployment

### Server Setup
- [ ] Linux server (Ubuntu 20.04+) deployed
- [ ] SSH access configured
- [ ] Firewall configured (port 5000)
- [ ] SSL certificate obtained
- [ ] Nginx installed and configured
- [ ] Systemd service created

### Application Setup
- [ ] Code deployed to `/opt/face-attendance/`
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Permissions set correctly
- [ ] Data directory writable
- [ ] Embeddings directory writable

### Service Configuration
- [ ] Systemd service file created
- [ ] Service enabled: `sudo systemctl enable face-attendance`
- [ ] Service started: `sudo systemctl start face-attendance`
- [ ] Service status checked: `sudo systemctl status face-attendance`
- [ ] Service logs accessible: `sudo journalctl -u face-attendance -f`

### Nginx Configuration
- [ ] Nginx config created
- [ ] SSL certificate configured
- [ ] Reverse proxy configured
- [ ] Static files served
- [ ] CORS headers configured
- [ ] Nginx restarted: `sudo systemctl restart nginx`

### Monitoring & Logging
- [ ] Application logs configured
- [ ] Error logs monitored
- [ ] Access logs monitored
- [ ] CPU usage monitored
- [ ] Memory usage monitored
- [ ] Disk usage monitored
- [ ] Alerts configured

### Backup & Recovery
- [ ] Backup script created
- [ ] Backup schedule configured
- [ ] Backup location verified
- [ ] Restore procedure tested
- [ ] Recovery time objective (RTO) defined
- [ ] Recovery point objective (RPO) defined

---

## Post-Deployment Verification

### Functionality Testing
- [ ] Face detection working
- [ ] Face recognition working
- [ ] Attendance logging working
- [ ] Time tracking working
- [ ] Notifications working
- [ ] Attendance viewer working
- [ ] CSV export working
- [ ] API endpoints working

### Performance Testing
- [ ] Response time < 100ms
- [ ] Face detection < 50ms/frame
- [ ] No memory leaks
- [ ] CPU usage normal
- [ ] Disk usage normal
- [ ] Network latency acceptable

### Security Testing
- [ ] HTTPS working
- [ ] SSL certificate valid
- [ ] CORS properly configured
- [ ] Input validation working
- [ ] Error messages safe
- [ ] No sensitive data exposed
- [ ] Firewall rules working

### Load Testing
- [ ] Single user working
- [ ] Multiple concurrent users working
- [ ] High load handled gracefully
- [ ] No crashes or errors
- [ ] Performance acceptable under load

---

## Documentation

### Deployment Documentation
- [ ] Installation guide created
- [ ] Configuration guide created
- [ ] Troubleshooting guide created
- [ ] API documentation updated
- [ ] User guide created
- [ ] Admin guide created

### Code Documentation
- [ ] Code comments added
- [ ] Docstrings added
- [ ] README updated
- [ ] CHANGELOG updated
- [ ] Version number updated

---

## Rollback Plan

### Rollback Procedure
- [ ] Previous version backed up
- [ ] Rollback script created
- [ ] Rollback tested
- [ ] Rollback time < 5 minutes
- [ ] Data integrity verified after rollback
- [ ] Services restored after rollback

### Disaster Recovery
- [ ] Disaster recovery plan created
- [ ] Backup locations verified
- [ ] Recovery procedures tested
- [ ] Recovery time acceptable
- [ ] Data loss acceptable

---

## Sign-Off

### Deployment Approval
- [ ] Technical lead approval: _______________
- [ ] Project manager approval: _______________
- [ ] Operations approval: _______________
- [ ] Security approval: _______________

### Deployment Date
- [ ] Scheduled date: _______________
- [ ] Actual deployment date: _______________
- [ ] Deployment duration: _______________
- [ ] Issues encountered: _______________

### Post-Deployment Review
- [ ] All systems operational
- [ ] No critical issues
- [ ] Performance acceptable
- [ ] Users satisfied
- [ ] Documentation complete

---

## Maintenance Schedule

### Daily Tasks
- [ ] Check system health
- [ ] Monitor error logs
- [ ] Verify backups completed
- [ ] Check disk space

### Weekly Tasks
- [ ] Review performance metrics
- [ ] Check security logs
- [ ] Update dependencies (if needed)
- [ ] Test backup restoration

### Monthly Tasks
- [ ] Full system backup
- [ ] Security audit
- [ ] Performance optimization
- [ ] Documentation review

### Quarterly Tasks
- [ ] Major version updates
- [ ] Security patches
- [ ] Capacity planning
- [ ] Disaster recovery drill

---

## Contact Information

### Support Contacts
- **Technical Support**: _______________
- **Operations**: _______________
- **Security**: _______________
- **Management**: _______________

### Escalation Procedure
1. Contact technical support
2. If unresolved, contact operations
3. If critical, contact management
4. Document all issues

---

## Notes

```
Additional notes and observations:
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
```

---

**Deployment Checklist Version**: 1.1
**Last Updated**: November 26, 2025
**Status**: Ready for Deployment

