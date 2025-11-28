import os
import sys
import time
import subprocess
from pyngrok import ngrok

# ==========================================
# PASTE YOUR TOKEN BELOW IF YOU WANT
# Example: NGROK_AUTH_TOKEN = "2q..."
# ==========================================
NGROK_AUTH_TOKEN = "367fJJuvqDYWWu2tUf5Ou4YXMDs_3v88q7ufSWESQ1iKfXZt1" 
# ==========================================

def main():
    print("===================================================")
    print("   Face Attendance System - Secure Mobile Access   ")
    print("===================================================")
    
    # Set auth token if provided in the script
    if NGROK_AUTH_TOKEN and NGROK_AUTH_TOKEN != "":
        print(f"[Info] Using hardcoded auth token...")
        ngrok.set_auth_token(NGROK_AUTH_TOKEN)

    print("\n[1/3] Starting Streamlit App...")
    
    # Start Streamlit in the background
    streamlit_cmd = [sys.executable, "-m", "streamlit", "run", "streamlit_app.py", "--server.headless", "true"]
    process = subprocess.Popen(streamlit_cmd)
    
    print("[2/3] Establishing Secure Tunnel (ngrok)...")
    try:
        # Open a HTTP tunnel on the default port 8501
        public_url = ngrok.connect(8501).public_url
        print(f"\n✅ SUCCESS! Your app is live at:\n")
        print(f"   👉  {public_url}  👈")
        print(f"\n   (Open this URL on your phone to access the camera)")
        print("\n[3/3] App is running. Press Ctrl+C to stop.")
        
        # Keep the script running
        process.wait()
        
    except KeyboardInterrupt:
        print("\nStopping...")
        process.terminate()
        ngrok.kill()
        sys.exit(0)
    except Exception as e:
        error_msg = str(e)
        print(f"\n❌ Error: {error_msg}")
        
        if "ERR_NGROK_107" in error_msg or "authentication failed" in error_msg:
            print("\n===================================================")
            print("🔴 AUTHENTICATION FAILED")
            print("===================================================")
            print("The token you entered is INVALID or EXPIRED.")
            print("Please get a new token from: https://dashboard.ngrok.com/get-started/your-authtoken")
            print("Then update the NGROK_AUTH_TOKEN variable in this file.")
        else:
            print("\nNote: If you see an authentication error, you may need to sign up for a free ngrok account")
            print("and run: ngrok config add-authtoken <token>")
            
        process.terminate()
        sys.exit(1)

if __name__ == "__main__":
    main()
