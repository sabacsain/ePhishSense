from flask import Flask, jsonify, request, session
from flask_cors import CORS
from extractor import GMAIL_EXTRACTOR
from extension_dt_model import DT_MODEL
from login import LOGIN
from encrypt import ENCRYPT
from decrypt import DECRYPT
import imaplib, secrets

app = Flask(__name__)
CORS(app)
# Generate random key
app.secret_key = secrets.token_hex(16)
# Set the session to only be transmitted via HTTPS
app.config['SESSION_COOKIE_SECURE'] = True
# Set the session to prevent client-side Javascript access
app.config['SESSION_COOKIE_HTTPONLY'] = True
# Protect against XSS/CSRF attacks
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
# Configure session to use a filesystem backend
app.config['SESSION_TYPE'] = 'filesystem'
# CORS(app, resources={r"/api/*": {"origins": "*"}})



@app.route('/api/login', methods=['POST'])
def login():    
    try:
        # Get value from login text fields in js
        data = request.get_json()

        # Access emailInput and passInput from the JSON data
        email_input = data.get('email', '')
        pass_input = data.get('password', '')

        # Execute login.py
        run = LOGIN(email_input, pass_input)

        # Return if not authenticated
        if not (run.get_authentication()):
            session['is_authenticated'] = False
            return jsonify({'message': 'Login FAILED'})

        # Set True since given creds are authenticated
        session['is_authenticated'] = True
        print(f'LOGIS_AUTH: {session["is_authenticated"]}')

        # Get mail object
        g_mail = run.get_mail()

        if not func_encrypt(g_mail, email_input, pass_input):
            return jsonify({'message' : 'Error in Encryption'})

        print(f'LOGkey: {session["key"]}')
        print(f'LOGdata: {session["encyrpted_Data"]}')

        # Clear data
        email_input = ''
        pass_input = '' 
        g_mail = ''

        return jsonify({'message': 'Login SUCCESSFUL'})

    except Exception as e:
        # Handle exceptions appropriately
        print('Error processing login:', str(e))
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/api/subject', methods=['POST'])
def subject():
    global input_subject

    # Get data from GUI
    data = request.get_json()

    # Extract subject from data variable
    input_subject = data.get('data', '')

    # Send a response back to GUI
    return jsonify({'message': 'Input Subject has been RECEIVED'})

@app.route('/api/scan', methods=['GET'])
def scan():
    try:
        # Randomize app session key again
        # app.secret_key = secrets.token_hex(16)

        # Check if authenticated
        if not session.get('is_authenticated', True):
            return jsonify({'message': 'Not authenticated'})

        print(f'IS_AUTH: {session["is_authenticated"]}')
        
        # Store data in temp variables
        if not session.get('key', True):
            return jsonify({'message': 'No key'})
        key = session.get('key')
        encrypted_data = session.get('encrypted_data')

        # CURRENT VALUE IS NONE
        print(f"key: {key}")
        print(f"DaTA: {encrypted_data}")

        # Decrypt login credentials
        if not func_decrypt(key, encrypted_data):
            return jsonify({'message': 'Error in Decryption'})

        # Clear data
        key = ''
        encrypted_data = ''

        # Store data in temp variables
        decrypted_data = session.get('decrypted_data')

        # Login using the decrypted credentials
        g_mail = imaplib.IMAP4_SSL(decrypted_data['server'], decrypted_data['port'])
        g_mail.login(decrypted_data['email'], decrypted_data['password'])

        # Check login credentials
        if not g_mail:
            return jsonify({'message': 'Error logging in'})

        # Encrypt back again the login credentials
        if not func_encrypt(g_mail, decrypted_data['email'], decrypted_data['password']):
                return jsonify({'message' : 'Error in Encryption'})

        # Clear data
        decrypted_data = ''

        # Extract Email

        run = GMAIL_EXTRACTOR(input_subject, g_mail)

        # Check if no subject found
        if not run.get_is_subject_found():
            return jsonify({'message': 'No subject found in the mailbox'})

        # Clear data
        g_mail = ''

        # Store numeric email value
        input = run.value()

        # Compare Email to the Model
        predict = DT_MODEL(input)
        prediction = predict.result()

        print(input)
        print(prediction)
        
        # Send the prediction to GUI
        return jsonify({'message': prediction})
    
    except Exception as e:
        
        print('ERROR_PATH: app.py in scan()')
        print(f'ERROR: {e}')

        if 'is_authenticated' or 'key' in str(e):
            return jsonify({'message': 'Authentication error'})

        return jsonify({'message': 'Error'})

@app.route('/api/main', methods=['GET'])
def main():

    return 
    

def func_encrypt(g_mail, email_input, pass_input):
    try: 
        # Encrypt mail object
        run_encrypt = ENCRYPT(g_mail, email_input, pass_input)

        # Get encryption key and encrypted data
        session['key'] = run_encrypt.get_key()

        # Store encrypted_data in the session
        session['encrypted_data'] = run_encrypt.get_encrypted()

        return True
    
    except Exception as e:
        print(f'ERROR: in func_encrypt \n{e}')
        return False


def func_decrypt(key, encrypted_data):
    try:
        # Decrypt login credentials
        print(key)
        print(encrypted_data)
        run_decrypt = DECRYPT(key, encrypted_data)
        print('nromans')
        session['decrypted_data'] = run_decrypt.get_decrypted()
        return True
    except Exception as e:
        print(f'ERROR: in func_decrypt \n{e}')
        return False
   
if __name__ == '__main__':
    app.run(debug=True)
