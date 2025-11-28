import sys
from pyngrok import ngrok

def main():
    print("===================================================")
    print("   Ngrok Setup (Python Version)   ")
    print("===================================================")
    print("This script will save your authtoken so you don't need to enter it again.")
    print("1. Get your token from: https://dashboard.ngrok.com/get-started/your-authtoken")
    print("2. Copy it.")
    print("---------------------------------------------------")
    
    token = input("Paste your Authtoken here: ").strip()
    
    if not token:
        print("Error: Token cannot be empty.")
        input("Press Enter to exit...")
        return

    try:
        ngrok.set_auth_token(token)
        print("\nSUCCESS! Token saved.")
        print("You can now run 'run_mobile.bat'.")
    except Exception as e:
        print(f"\nError saving token: {e}")
    
    print("---------------------------------------------------")
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
