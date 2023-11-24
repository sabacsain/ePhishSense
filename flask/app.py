# app.py
from flask import Flask, redirect, request, session, jsonify
import requests, imaplib, base64
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

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

    # Check if the response includes a refresh token
    refresh_token = token_json.get("refresh_token")
    if refresh_token:
        session["refresh_token"] = refresh_token

    session['oauth_token'] = token_json
    print(refresh_token)
    print('normans')
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


from google.auth.exceptions import RefreshError

def authenticate_email(token):
    try:
        # Ensure the token has the necessary information
        required_fields = ['client_id', 'client_secret', 'refresh_token', 'token', 'token_uri']
        if not all(field in token for field in required_fields):
            raise ValueError("Authorized user info is missing required fields.")

        # Create a Gmail API service
        creds = Credentials.from_authorized_user_info(
            token,
            scopes=['https://www.googleapis.com/auth/gmail.readonly'],  # Add necessary scopes
            redirect_uri="http://localhost:5000/oauth_callback"  # Replace with your redirect URI
        )

        # Call the Gmail API to get the user's Gmail profile
        service = build('gmail', 'v1', credentials=creds)
        profile = service.users().getProfile(userId='me').execute()

        # Fetch the latest email from the inbox
        messages = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=1).execute()
        if 'messages' in messages:
            latest_message_id = messages['messages'][0]['id']
            message = service.users().messages().get(userId='me', id=latest_message_id).execute()
            subject = message['subject']
            body = base64.urlsafe_b64decode(message['payload']['body']['data']).decode('utf-8')
            print(f"Latest Email Subject: {subject}")
            print(f"Latest Email Body:\n{body}")

        return True

    except RefreshError:
        print("Token refresh failed. The access token might be expired.")
        return False
    except ValueError as ve:
        print(f"Login FAILED: {ve}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False




if __name__ == "__main__":
    app.run(debug=True)
