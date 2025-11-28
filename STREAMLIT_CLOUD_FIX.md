# **CRITICAL: You MUST do this in Streamlit Cloud**

The app is using Python 3.13 which doesn't support MediaPipe.

## Steps to Fix:

###1. Go to Streamlit Cloud Dashboard
- Go to https://share.streamlit.io
- Find your app "Face-Attendance-System"

### 2. DELETE the App
- Click "⋮" (three dots) next to your app
- Click "Delete app"
- Confirm deletion

### 3. Create New App
- Click "New app"
- Select your repository: `addygeek/Face-Attendance-System`
- Set:
  - **Branch**: `main`
  - **Main file path**: `streamlit_app.py`
  - **Python version**: Select **3.11** from dropdown (NOT 3.13!)

### 4. Deploy
- Click "Deploy"
- Wait 2-5 minutes

## Why This is Needed
Streamlit Cloud is caching the old Python 3.13 environment. Deleting and recreating forces it to use Python 3.11 properly.

## Alternative: Reboot App
If you don't want to delete:
1. Go to "Manage app" → "⋮" → "Reboot app"
2. If that doesn't work, try "Settings" → Check Python version is set to 3.11
3. If still failing, you MUST delete and recreate

The `.python-version` file is now set to `3.11.0` which should work.
