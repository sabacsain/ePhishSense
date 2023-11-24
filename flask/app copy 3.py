# app.py
from flask import Flask, redirect, request, session, jsonify
import requests, imaplib, base64

app = Flask(__name__)
app.secret_key = 'decisionTree5*'  # Change this to a secure secret key

# Replace with your actual client ID and client secret
client_id = '975763760963-7u67rrok2gmehpsbd7t2slp2mdrgieha.apps.googleusercontent.com'
client_secret = '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'

authorization_base_url = "https://accounts.google.com/o/oauth2/auth"
token_url = "https://accounts.google.com/o/oauth2/token"

@app.route("/")
def index():
    # Redirect the user to the Gmail OAuth page with the specified scope and redirect_uri
    redirect_uri = "http://localhost:5000/oauth_callback"
    scope = ["https://www.googleapis.com/auth/gmail.readonly"]

    authorization_url = (
        f"{authorization_base_url}?response_type=code&client_id={client_id}"
        f"&redirect_uri={redirect_uri}&scope={'+'.join(scope)}"
    )
    return redirect(authorization_url)

@app.route("/oauth_callback")
def oauth_callback():
    # Handle the OAuth callback and retrieve access token from the redirect URI query parameter
    redirect_uri = "http://localhost:5000/oauth_callback"
    code = request.args.get('code')

    token_url = "https://accounts.google.com/o/oauth2/token"
    token_data = {
        'code': code,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code',
    }

    # Use requests library to exchange the authorization code for an access token
    token_response = requests.post(token_url, data=token_data)
    token_json = token_response.json()
    session['oauth_token'] = token_json

    return redirect("/emails")

@app.route("/emails")
def fetch_emails():
    # Retrieve the stored token from the session
    token = session.get("oauth_token")

    if not token:
        return redirect("/")

    if not authenticate_email(token):
        return "Email not authenticated"

    # Use the token to fetch emails via Gmail API or perform other actions
    # Add your Gmail API request logic here

    return "Emails fetched successfully!"

def authenticate_email(token):
    # some code
    try:
        pass
        return "LOGIN SUCCESSFUL"
    
    except Exception as e:
        print(f"Login Failed: {e}")
        return "LOGIN FAILED"

if __name__ == "__main__":
    app.run(debug=True)
