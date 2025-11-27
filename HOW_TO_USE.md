# 🚀 How to Use Your Face Recognition System

## ✅ System Setup Complete!

Your face recognition system is now **FULLY TRAINED** and ready to use for 3 people:
- **Aditya** (9 training images)
- **Sanu** (4 training images)
- **Person** (4 training images) - *Consider renaming this folder to the actual person's name*

---

## 🎯 Running the System

### Step 1: Start the Backend Server

Open a terminal and run:

```powershell
cd "d:\PROGRAMING\7th sem 7\face\face_detection_app\ml_model"
..\.venv311\Scripts\python.exe app.py
```

**You should see:**
```
* Serving Flask app 'app'
* Debug mode: on
* Running on http://127.0.0.1:5000
```

> [!IMPORTANT]
> **Keep this terminal window open!** The server must be running for the web app to work.

### Step 2: Open the Web Application

1. Navigate to: `d:\PROGRAMING\7th sem 7\face\face_detection_app\web_app\`
2. Open `index.html` in your web browser
3. Allow camera access when prompted

---

## 📹 Using Face Detection

### What You'll See

When faces are detected, the system annotates them with colored boxes:

| Box Color | Label | Meaning | Example |
|-----------|-------|---------|---------|
| 🟢 **Green** | **ADITYA** | Aditya recognized with high confidence | Aditya's face matches training data |
| 🟢 **Green** | **SANU** | Sanu recognized with high confidence | Sanu's face matches training data |
| 🟢 **Green** | **PERSON** | Third person recognized | Face in "Person" folder detected |
| 🔴 **Red** | **Person** | Unknown/unrecognized face | Face doesn't match any training data |

### Automatic Attendance Logging

When a **known person** is detected (green box):
- Attendance is automatically logged every 30 seconds
- A green notification appears in the top-right corner
- Timestamp and confidence score are recorded

---

## 📊 Viewing Attendance Records

1. Open `attendance.html` in your browser
2. View all logged attendance records
3. Filter by:
   - Person name (e.g., "Aditya")
   - Date (YYYY-MM-DD format)
4. Delete records if needed
5. Export data as CSV (if implemented)

---

## 👤 Registering New People

### Option 1: Using the Web Interface (Quick)

1. Open `register.html` in your browser
2. Enter the person's name
3. Position face in camera
4. Click "Save Embedding"
5. System will recognize this person immediately

### Option 2: Training from Multiple Images (Better Accuracy)

1. **Create a folder** with the person's name:
   ```powershell
   cd "d:\PROGRAMING\7th sem 7\face\face_detection_app\ml_model\data"
   mkdir "NewPersonName"
   ```

2. **Add 5-10 clear face images** to the folder:
   - Good lighting
   - Different angles
   - Clear facial features
   - JPG or PNG format

3. **Retrain the system:**
   ```powershell
   cd "d:\PROGRAMING\7th sem 7\face\face_detection_app\ml_model"
   ..\.venv311\Scripts\python.exe register.py
   ```

4. **Copy embeddings to web app:**
   ```powershell
   copy output\*.json ..\web_app\embeddings\
   ```

5. **Refresh the web page** to load new embeddings

---

## 🔧 Configuration & Tuning

### Adjusting Recognition Sensitivity

Edit [`web_app/script.js`](file:///d:/PROGRAMING/7th%20sem%207/face/face_detection_app/web_app/script.js#L6):

```javascript
const THRESHOLD = 0.1; // Similarity threshold
```

- **Lower value (e.g., 0.05)**: More lenient, may have false positives
- **Higher value (e.g., 0.15)**: More strict, may miss actual people

### Attendance Logging Interval

Edit [`web_app/script.js`](file:///d:/PROGRAMING/7th%20sem%207/face/face_detection_app/web_app/script.js#L8):

```javascript
const ATTENDANCE_LOG_INTERVAL = 30000; // 30 seconds
```

Change this value (in milliseconds) to adjust how often attendance is logged for the same person.

### Recognition Update Rate

Edit [`web_app/script.js`](file:///d:/PROGRAMING/7th%20sem%207/face/face_detection_app/web_app/script.js#L13):

```javascript
const VERIFY_INTERVAL = 200; // 200ms
```

- **Lower value**: More responsive, higher CPU usage
- **Higher value**: Less responsive, lower CPU usage

---

## 🐛 Troubleshooting

### Face Not Detected

**Problem:** No bounding boxes appear

**Solutions:**
- Ensure good lighting
- Position face directly toward camera
- Check if camera is working (test in other apps)
- Verify browser has camera permissions

### Shows "Person" (Red Box) for Known People

**Problem:** System shows red box with "Person" label for Aditya/Sanu/Person

**Solutions:**
1. Check if Flask backend is running (`python app.py`)
2. Verify embeddings exist in `web_app/embeddings/`:
   ```powershell
   dir "d:\PROGRAMING\7th sem 7\face\face_detection_app\web_app\embeddings"
   ```
3. Refresh the web page (Ctrl+F5)
4. Check browser console for errors (F12 → Console tab)

### Embeddings Not Loading

**Problem:** Console shows "Could not load embeddings"

**Solutions:**
1. Ensure Flask server is running on port 5000
2. Check CORS settings in [`app.py`](file:///d:/PROGRAMING/7th%20sem%207/face/face_detection_app/ml_model/app.py#L9)
3. Verify embeddings are in correct location:
   - Training creates: `ml_model/output/*.json`
   - Web app needs: `web_app/embeddings/*.json`
4. Copy embeddings if missing:
   ```powershell
   copy "ml_model\output\*.json" "web_app\embeddings\"
   ```

### Attendance Not Logging

**Problem:** Green box shows but attendance doesn't log

**Solutions:**
1. Verify Flask backend is running
2. Check browser console for API errors (F12)
3. Ensure person is recognized (green box, not red)
4. Wait 30 seconds between logs (duplicate prevention)
5. Check data file exists: `data/attendance.json`

---

## 📁 Important File Locations

### Training Data
```
ml_model/data/
├── Aditya/          ← 9 training images
├── Sanu/            ← 4 training images
└── Person/          ← 4 training images (rename this!)
```

### Generated Embeddings
```
ml_model/output/     ← Training script saves here
web_app/embeddings/  ← Web app loads from here
```

### Attendance Records
```
data/attendance.json ← All attendance logs stored here
```

---

## 🎨 How Face Annotation Works

The system uses **MediaPipe Face Mesh** to detect faces and extract 478 facial landmarks. Here's the process:

1. **Detection**: Camera captures frames → MediaPipe detects faces
2. **Embedding**: Extracts facial features into a numerical vector (1419 dimensions)
3. **Comparison**: Compares with saved embeddings using cosine similarity
4. **Annotation**: Draws colored box with person's name if match found
5. **Logging**: Records attendance for recognized people

### Annotation Code Flow

```javascript
// From script.js lines 114-138
if (similarity >= THRESHOLD) {
  // Known person - GREEN BOX
  return { 
    name: "ADITYA" or "SANU" or "PERSON",
    color: "#00FF00",  // Green
    confidence: similarity 
  };
} else {
  // Unknown person - RED BOX
  return { 
    name: "Person",
    color: "#FF0000",  // Red
    confidence: similarity 
  };
}
```

---

## 💡 Tips for Best Results

### Training Data Quality
- Use **8-10 images** per person for better accuracy
- Include **different angles** (front, slightly left, slightly right)
- Ensure **good lighting** (avoid shadows on face)
- Use **clear, high-resolution** images
- Have person **look directly at camera** in most images

### Real-Time Detection
- Position face **1-2 feet from camera**
- Ensure **even lighting** (avoid backlighting)
- Keep face **clearly visible** (no obstructions)
- Look **toward camera** for best recognition

### System Performance
- Close other camera applications
- Use a good quality webcam
- Ensure adequate CPU resources
- Run in Chrome/Edge for best compatibility

---

## 🔄 Renaming "Person" Folder

The third person's folder is currently named "Person". Here's how to rename it:

```powershell
# Navigate to data directory
cd "d:\PROGRAMING\7th sem 7\face\face_detection_app\ml_model\data"

# Rename folder (replace "ActualName" with the real name)
ren Person ActualName

# Retrain embeddings
cd ..
..\.venv311\Scripts\python.exe register.py

# Copy new embeddings
copy output\*.json ..\web_app\embeddings\
```

---

## 📝 Next Steps

**Immediate:**
1. ✅ Start Flask server: `..\.venv311\Scripts\python.exe app.py`
2. ✅ Open `web_app/index.html` in browser
3. ✅ Test face detection with Aditya, Sanu, and Person
4. ✅ Check attendance logging in `web_app/attendance.html`

**Optional Improvements:**
- Rename "Person" folder to actual name
- Add more training images for better accuracy
- Add more people to the system
- Adjust similarity threshold if needed
- Customize UI colors/styles in `web_app/styles.css`

---

## 🆘 Getting Help

If you encounter issues:
1. Check this guide's troubleshooting section
2. View browser console for errors (F12 → Console)
3. Check Flask terminal for backend errors
4. Verify all file paths are correct
5. Ensure Python 3.11.9 (`.venv311`) is being used, not 3.13

**Common Issue:** MediaPipe doesn't support Python 3.13+, must use Python 3.11 or lower!

---

## ✨ System Status

| Component | Status | Notes |
|-----------|--------|-------|
| Training Data | ✅ Ready | 3 people with images |
| Embeddings | ✅ Generated | All 3 people trained |
| Backend API | ✅ Running | Flask on port 5000 |
| Web Interface | ✅ Ready | Open index.html |
| Face Detection | ✅ Working | MediaPipe Face Mesh |
| Annotation | ✅ Active | Green/Red boxes |
| Attendance | ✅ Logging | Auto-logs every 30s |

**Your system is fully operational and ready to use!** 🎉
