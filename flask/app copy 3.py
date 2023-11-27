from flask import Flask, jsonify, request
from extractor import GMAIL_EXTRACTOR
from extension_dt_model import DT_MODEL
from login import LOGIN
from encrypt import ENCRYPT
from decrypt import DECRYPT
import os, imaplib

app = Flask(__name__)

# Initialize global variables
# is_authenticated = False
# g_mail = None
# key = ''
# temp_path = ''
# encrypted_data = ''

@app.route('/api/login', methods=['POST'])
def login():
    global g_mail, key, encrypted_data, is_authenticated
    is_authenticated = False
    
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
            return jsonify({'message': 'Login FAILED'})

        # Set True since given creds is authenticated
        is_authenticated = True

        # Get mail object
        g_mail = run.get_mail()

        if not func_encrypt(g_mail, email_input, pass_input):
            return jsonify({'message' : 'Error in Encryption'})
        # # Encrypt mail object
        # run_encrypt = ENCRYPT(g_mail, email_input, pass_input)

        # # Get encryption key and encrypted data
        # key = run_encrypt.get_key()
        # # temp_path = run_encrypt.get_path()
        # encrypted_data = run_encrypt.get_encrypted()

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
    return jsonify({'message': 'Input Subject Received Successfully'})

@app.route('/api/scan', methods=['GET'])
def scan():
    global input_subject, g_mail, key, encrypted_data, is_authenticated, decrypted_data

    # Check if authenticated
    if not is_authenticated:
        return jsonify({'message': 'Not authenticated'})

    # Decrypt login credentials
    if not func_decrypt(key, encrypted_data):
        return jsonify({'message': 'Error in Decryption'})
    # run_decrypt = DECRYPT(key, encrypted_data)
    # decrypted_data = run_decrypt.get_decrypted()

    # Login using the decrypted credentials
    g_mail = imaplib.IMAP4_SSL(decrypted_data['server'], decrypted_data['port'])
    g_mail.login(decrypted_data['email'], decrypted_data['password'])

    # Check login credentials
    if not g_mail:
        return jsonify({'message': 'Error logging in'})

    # Extract Email
    run = GMAIL_EXTRACTOR(input_subject, g_mail)

    if not run.get_is_mailbox_empty():
        return jsonify({'message': 'Inbox is empty'})

    # Store numeric email value
    input = run.value()

    # Encrypt back again the login credentials
    if not func_encrypt(g_mail, decrypted_data['email'], decrypted_data['password']):
            return jsonify({'message' : 'Error in Encryption'})

    # Clear data
    decrypted_data = ''
    g_mail = ''

    # Compare Email to the Model
    predict = DT_MODEL(input)
    prediction = predict.result()

    print(input)
    print(prediction)
    
    # Send the prediction to GUI
    return jsonify({'message': prediction})

@app.route('/api/main', methods=['GET'])
def main():

    return 
    

def func_encrypt(g_mail, email_input, pass_input):
    global key, encrypted_data
    try: 
        # Encrypt mail object
        run_encrypt = ENCRYPT(g_mail, email_input, pass_input)

        # Get encryption key and encrypted data
        key = run_encrypt.get_key()
        # temp_path = run_encrypt.get_path()
        encrypted_data = run_encrypt.get_encrypted()
        return True
    
    except Exception as e:
        print(f'ERROR: in func_encrypt \n{e}')
        return False


def func_decrypt(key, encrypted_data):
    global decrypted_data
    try:
        # Decrypt login credentials
        run_decrypt = DECRYPT(key, encrypted_data)
        decrypted_data = run_decrypt.get_decrypted()
        return True
    except Exception as e:
        print(f'ERROR: in func_encrypt \n{e}')
        return False
   
if __name__ == '__main__':
    app.run(debug=True)
