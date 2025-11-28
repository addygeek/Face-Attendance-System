# Mobile Access Guide (HTTPS Fix)

To use the camera on your phone, the website **MUST** be served over **HTTPS**. Browsers block camera access on insecure (HTTP) connections unless it's `localhost`.

## How to Run on Phone

I have added a tool called `ngrok` that creates a secure tunnel for you.

### Step 1: Start the Secure App
Double-click the **`run_mobile.bat`** file in your folder.

### Step 2: Get the Link
A command window will open and show a link like:
`https://<random-id>.ngrok-free.app`

### Step 3: Open on Phone
Type that link into your phone's browser. The camera should now work!

---

## Troubleshooting

### "Authentication Failed" Error
If you see an error about authentication, you need to configure your free ngrok account.

1.  Double-click **`setup_ngrok.bat`**.
2.  Follow the instructions to get your free token from ngrok.com.
3.  Paste the token when asked.
4.  Run `run_mobile.bat` again.

### Permanent Solution
For a permanent link that doesn't change, you should deploy the app to **Streamlit Cloud** or **Render** using the `DEPLOY_FIXES.md` guide I created earlier. They provide free HTTPS automatically.
