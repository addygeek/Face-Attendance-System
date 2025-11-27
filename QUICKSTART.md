# Quick Start Guide

Get the face attendance system running in 5 minutes!

## Prerequisites

- Python 3.9+ (3.13 tested)
- Webcam
- Modern web browser (Chrome, Firefox, Safari, Edge)

## Step 1: Install Dependencies (2 min)

### Option A: Windows
```bash
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install core dependencies
pip install numpy opencv-python flask flask-cors

# Install MediaPipe (try this first)
pip install --no-cache-dir mediapipe

# If MediaPipe fails, use Conda instead (see Option C)
```

### Option B: Mac/Linux
```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install core dependencies
pip install numpy opencv-python flask flask-cors

# Install MediaPipe
pip install --no-cache-dir mediapipe
```

### Option C: Using Conda (Recommended if pip fails)
```bash
# Install Conda from: https://www.anaconda.com/download

# Create environment
conda create -n face-attendance python=3.11

# Activate
conda activate face-attendance

# Install all dependencies
conda install numpy opencv flask flask-cors mediapipe
```

**Note:** If MediaPipe installation fails, see [INSTALLATION_WORKAROUND.md](INSTALLATION_WORKAROUND.md) for alternative methods.

## Step 2: Prepare Training Data (Optional - 1 min)

**Option A: With Training Data (Recommended)**
1. Create folder: `ml_model/data/YourName/`
2. Add 8-10 clear face images to this folder
3. Images should be JPG or PNG format

**Option B: Without Training Data (Use Default "Person")**
- Skip this step
- System will use "Person" as default name
- All detected faces will be labeled "Person"

## Step 3: Train Model (Optional - 1 min)

If you added training data:

### Windows
```bash
cd ml_model
python register.py
```

### Mac/Linux
```bash
cd ml_model
python3 register.py
```

You should see:
```
Processing YourName: image1.jpg
Processing YourName: image2.jpg
...
✔ Saved: embeddings/YourName_embedding.json
```

## Step 4: Start Backend (30 sec)

### Windows
```bash
cd ml_model
python app.py
```

### Mac/Linux
```bash
cd ml_model
python3 app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
```

## Step 5: Open Web Interface (30 sec)

1. Open `web_app/index.html` in your browser
2. Allow camera access when prompted
3. You should see live video feed with face detection

## Done! 🎉

Now you can:

- **Detect faces**: Look at the camera
  - Green box = Known person (if trained)
  - Red box = Unknown person
  - Orange box = Default "Person" (if no embeddings)
  
- **Automatic logging**: Attendance is logged automatically when a face is detected
  - Shows person name and time
  - Prevents duplicate logs (30-second interval)
  
- **Register new people**: Go to "Register Face" page
  - Enter person's name
  - Position face in camera
  - Click "Save Embedding"
  
- **View attendance**: Go to "View Attendance" page
  - See all logged records
  - Filter by name and date
  - View time ranges (start to end)
  - Export to CSV

## Default Behavior

**Without Training Data:**
- All detected faces labeled as "Person"
- Attendance logged with "Person" name
- Shows time range for each detection

**With Training Data:**
- Recognized people show their name
- Unknown people show "Person"
- Attendance logged with actual name

## Common Issues

**"No face detected"**
- Ensure good lighting
- Position face directly toward camera
- Check camera permissions in browser

**"API connection error"**
- Make sure backend is running
- Check that port 5000 is available
- Try: `netstat -an | findstr 5000` (Windows) or `lsof -i :5000` (Mac)

**"Embeddings not loading"**
- Check `web_app/embeddings/` folder
- Verify embedding files exist
- Check browser console (F12) for errors

**"MediaPipe installation failed"**
- See [INSTALLATION_WORKAROUND.md](INSTALLATION_WORKAROUND.md)
- Try Conda: `conda install mediapipe`
- Or use API-only mode without face detection

## Next Steps

1. **Add more people**: Create folders in `ml_model/data/` and run `python register.py` again
2. **Customize threshold**: Edit `THRESHOLD` in `web_app/script.js` (default: 0.1)
3. **Export attendance**: Use "Export CSV" button on attendance page
4. **Deploy to production**: See `DEPLOYMENT.md`

## Full Documentation

- **Complete Guide**: See `README.md`
- **API Reference**: See `API_DOCUMENTATION.md`
- **Storage Details**: See `JSON_STORAGE_GUIDE.md`
- **Deployment**: See `DEPLOYMENT.md`
