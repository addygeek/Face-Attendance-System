# Streamlit Face Attendance App - Quick Start Guide

This guide explains how to run the new Streamlit-based Face Attendance System.

## 1. Installation

First, ensure you have the required dependencies installed. Open your terminal in the project directory:

```bash
pip install -r ml_model/requirements.txt
```

## 2. Running the App

To start the application, run:

```bash
streamlit run streamlit_app.py
```

This will open the app in your default web browser (usually at `http://localhost:8501`).

## 3. Using the App

### Home (Attendance)
- Allow camera access when prompted.
- The app will detect faces in real-time.
- **Green Box**: Known person (Attendance logged).
- **Red Box**: Unknown person.
- **Blue/No Box**: No face detected or low confidence.

### Register Face
1. Go to the **Register Face** page from the sidebar.
2. Enter the person's **Name**.
3. Look at the camera and click **Take a picture**.
4. Click **Save Face** to generate and save the embedding.

### View Logs
- Go to **View Logs** to see the attendance history.
- You can refresh or clear the logs.

## 4. Mobile Access (Local Network)

To access the app from your mobile phone while running it on your computer:

1. Ensure your phone and computer are on the **same Wi-Fi network**.
2. When you run `streamlit run`, it shows a **Network URL** (e.g., `http://192.168.1.5:8501`).
3. Open that URL in your phone's browser.
4. **Note**: For camera access on mobile browsers (non-localhost), you might need to use HTTPS or configure your browser to allow insecure origins for testing.
   - **Chrome (Android)**: Go to `chrome://flags/#unsafely-treat-insecure-origin-as-secure`, add your IP:Port, enable, and restart Chrome.

## 5. Cloud Deployment (Shareable Link)

To share with others easily, deploy to **Streamlit Community Cloud**:

1. Push your code to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io/).
3. Connect your GitHub account.
4. Select your repository and `streamlit_app.py` as the main file.
5. Click **Deploy**.
6. You will get a public URL (e.g., `https://your-app.streamlit.app`) that works on any device with HTTPS (Camera will work automatically).
