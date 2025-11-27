# Setup Guide - Windows & Mac

Complete step-by-step setup for both Windows and Mac.

---

## 🪟 WINDOWS Setup

### Step 1: Install Python

1. Download Python 3.13 from: https://www.python.org/downloads/
2. Run installer
3. **IMPORTANT**: Check "Add Python to PATH"
4. Click "Install Now"

### Step 2: Verify Python Installation

Open PowerShell and run:
```powershell
python --version
pip --version
```

You should see:
```
Python 3.13.x
pip 24.x.x
```

### Step 3: Create Virtual Environment

```powershell
# Navigate to project folder
cd path\to\face-attendance-system

# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\activate

# You should see (.venv) at the start of your prompt
```

### Step 4: Install Dependencies

```powershell
# Upgrade pip
python -m pip install --upgrade pip

# Install core dependencies
pip install numpy opencv-python flask flask-cors

# Install MediaPipe
pip install --no-cache-dir mediapipe
```

### Step 5: Verify Installation

```powershell
python -c "import cv2; import mediapipe; import flask; print('✓ All dependencies installed!')"
```

### Step 6: Prepare Training Data (Optional)

```powershell
# Create data folder
mkdir ml_model\data\YourName

# Add 8-10 face images to: ml_model\data\YourName\
```

### Step 7: Train Embeddings (Optional)

```powershell
cd ml_model
python register.py
cd ..
```

### Step 8: Start Backend

```powershell
cd ml_model
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
```

### Step 9: Open Web Interface

1. Open `web_app/index.html` in your browser
2. Allow camera access
3. Start detecting faces!

### Step 10: Stop Backend

Press `Ctrl + C` in PowerShell

---

## 🍎 MAC Setup

### Step 1: Install Python

**Option A: Using Homebrew (Recommended)**
```bash
# Install Homebrew if not installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.13
```

**Option B: Direct Download**
1. Download Python 3.13 from: https://www.python.org/downloads/
2. Run installer
3. Follow prompts

### Step 2: Verify Python Installation

```bash
python3 --version
pip3 --version
```

You should see:
```
Python 3.13.x
pip 24.x.x
```

### Step 3: Create Virtual Environment

```bash
# Navigate to project folder
cd path/to/face-attendance-system

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# You should see (.venv) at the start of your prompt
```

### Step 4: Install Dependencies

```bash
# Upgrade pip
python3 -m pip install --upgrade pip

# Install core dependencies
pip install numpy opencv-python flask flask-cors

# Install MediaPipe
pip install --no-cache-dir mediapipe
```

### Step 5: Verify Installation

```bash
python3 -c "import cv2; import mediapipe; import flask; print('✓ All dependencies installed!')"
```

### Step 6: Prepare Training Data (Optional)

```bash
# Create data folder
mkdir -p ml_model/data/YourName

# Add 8-10 face images to: ml_model/data/YourName/
```

### Step 7: Train Embeddings (Optional)

```bash
cd ml_model
python3 register.py
cd ..
```

### Step 8: Start Backend

```bash
cd ml_model
python3 app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
```

### Step 9: Open Web Interface

1. Open `web_app/index.html` in your browser
2. Allow camera access
3. Start detecting faces!

### Step 10: Stop Backend

Press `Ctrl + C` in Terminal

---

## 🐍 Using Conda (Alternative - Works on Both)

### Step 1: Install Conda

Download from: https://www.anaconda.com/download

### Step 2: Create Environment

```bash
# Windows or Mac
conda create -n face-attendance python=3.11

# Activate
conda activate face-attendance
```

### Step 3: Install Dependencies

```bash
conda install numpy opencv flask flask-cors mediapipe
```

### Step 4: Prepare Training Data (Optional)

```bash
# Windows
mkdir ml_model\data\YourName

# Mac
mkdir -p ml_model/data/YourName
```

### Step 5: Train Embeddings (Optional)

```bash
cd ml_model
python register.py
cd ..
```

### Step 6: Start Backend

```bash
cd ml_model
python app.py
```

### Step 7: Open Web Interface

Open `web_app/index.html` in browser

---

## 🚀 Quick Start Commands

### Windows (PowerShell)
```powershell
# Setup
python -m venv .venv
.venv\Scripts\activate
pip install numpy opencv-python flask flask-cors mediapipe

# Run
cd ml_model
python app.py

# In another PowerShell window
# Open web_app/index.html
```

### Mac (Terminal)
```bash
# Setup
python3 -m venv .venv
source .venv/bin/activate
pip install numpy opencv-python flask flask-cors mediapipe

# Run
cd ml_model
python3 app.py

# In another Terminal window
# Open web_app/index.html
```

---

## ✅ Verification Checklist

- [ ] Python 3.9+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed successfully
- [ ] `python -c "import cv2; import mediapipe; import flask"` works
- [ ] Backend starts without errors
- [ ] Web interface loads in browser
- [ ] Camera access granted
- [ ] Faces detected in real-time

---

## 🐛 Troubleshooting

### Issue: "Python not found"
**Windows:**
```powershell
# Check if Python is in PATH
python --version

# If not, reinstall Python and check "Add Python to PATH"
```

**Mac:**
```bash
# Use python3 instead of python
python3 --version
```

### Issue: "pip: command not found"
```bash
# Windows
python -m pip install --upgrade pip

# Mac
python3 -m pip install --upgrade pip
```

### Issue: "ModuleNotFoundError: No module named 'cv2'"
```bash
pip install opencv-python
```

### Issue: "ModuleNotFoundError: No module named 'mediapipe'"
```bash
# Try without cache
pip install --no-cache-dir mediapipe

# Or use Conda
conda install mediapipe
```

### Issue: "Port 5000 already in use"
```bash
# Windows - Find process using port 5000
netstat -ano | findstr :5000

# Mac - Find process using port 5000
lsof -i :5000

# Kill the process or use different port
```

### Issue: "Camera not working"
1. Check browser permissions (Settings → Privacy → Camera)
2. Ensure camera is not used by another app
3. Try different browser
4. Restart browser

### Issue: "No faces detected"
1. Ensure good lighting
2. Position face directly toward camera
3. Check camera is working (test in other app)
4. Try moving closer to camera

---

## 📝 Default Behavior

**Without Training Data:**
- All detected faces labeled as "Person"
- Attendance logged with "Person" name
- Shows time range for each detection

**With Training Data:**
- Recognized people show their name
- Unknown people show "Person"
- Attendance logged with actual name

---

## 🎯 Next Steps

1. **Add Training Data** (Optional)
   - Create `ml_model/data/YourName/` folder
   - Add 8-10 face images
   - Run `python register.py`

2. **Use the System**
   - Open `web_app/index.html`
   - Look at camera
   - Attendance logged automatically

3. **View Records**
   - Open `web_app/attendance.html`
   - See all logged attendance
   - Filter by name and date
   - Export to CSV

4. **Deploy to Production**
   - See `DEPLOYMENT.md`
   - Set up on server
   - Configure Nginx
   - Set up SSL

---

## 📞 Support

- **Quick Setup**: See `QUICKSTART.md`
- **Full Guide**: See `README.md`
- **API Reference**: See `API_DOCUMENTATION.md`
- **Troubleshooting**: See `INSTALLATION_WORKAROUND.md`

---

## ✨ Features

✅ Real-time face detection
✅ Automatic attendance logging
✅ Default "Person" name
✅ Time range tracking
✅ Attendance management
✅ CSV export
✅ REST API
✅ JSON storage (no database)

---

**Ready to use!** 🚀

