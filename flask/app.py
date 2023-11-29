from flask import Flask, render_template, jsonify, request, session
from extractor import GMAIL_EXTRACTOR
from extension_dt_model import DT_MODEL
from login import LOGIN
from encrypt import ENCRYPT
from decrypt import DECRYPT
import imaplib, secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_started')
def get_started():
    return render_template('get_started.html')

@app.route('/terms_and_conditions')
def terms_and_conditions():
    return render_template('terms_and_conditions.html')

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()

        email_input = data.get('email', '')
        pass_input = data.get('password', '')

        run = LOGIN(email_input, pass_input)

        if not run.get_authentication():
            session.clear()
            return jsonify({'message': 'Login FAILED'})

        session['is_authenticated'] = True
        g_mail = run.get_mail()

        if not func_encrypt(g_mail, email_input, pass_input):
            return jsonify({'message' : 'Error in Encryption'})

        email_input = ''
        pass_input = '' 
        g_mail = ''

        return jsonify({'message': 'Login SUCCESSFUL'})

    except Exception as e:
        print(f'Error processing login: {e}')
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/api/subject', methods=['POST'])
def subject():
    data = request.get_json()
    input_subject = data.get('data', '')
    return jsonify({'message': 'Input Subject has been RECEIVED'})

@app.route('/api/scan', methods=['GET'])
def scan():
    try:
        session.clear()

        if not session.get('is_authenticated', False):
            return jsonify({'message': 'Not authenticated'})

        key = session['key']
        encrypted_data = session['encrypted_data']

        if not func_decrypt(key, encrypted_data):
            return jsonify({'message': 'Error in Decryption'})

        key = ''
        encrypted_data = ''

        decrypted_data = session['decrypted_data']

        g_mail = imaplib.IMAP4_SSL(decrypted_data['server'], decrypted_data['port'])
        g_mail.login(decrypted_data['email'], decrypted_data['password'])

        if not g_mail:
            return jsonify({'message': 'Error logging in'})

        if not func_encrypt(g_mail, decrypted_data['email'], decrypted_data['password']):
            return jsonify({'message' : 'Error in Encryption'})

        decrypted_data = ''

        input_subject = session.get('input_subject', '')

        run = GMAIL_EXTRACTOR(input_subject, g_mail)

        if not run.get_is_subject_found():
            return jsonify({'message': 'No subject found in the mailbox'})

        g_mail = ''
        input = run.value()

        predict = DT_MODEL(input)
        prediction = predict.result()

        print(input)
        print(prediction)
        
        return jsonify({'message': prediction})
    
    except Exception as e:
        print(f'ERROR_PATH: app.py in scan()\nERROR: {e}')

        if 'is_authenticated' or 'key' in str(e):
            return jsonify({'message': 'Authentication error'})

        return jsonify({'message': 'Error'})

@app.route('/api/main', methods=['GET'])
def main():
    return jsonify({'message': 'Placeholder for /api/main'})

def func_encrypt(g_mail, email_input, pass_input):
    try: 
        run_encrypt = ENCRYPT(g_mail, email_input, pass_input)
        session['key'] = run_encrypt.get_key()
        session['encrypted_data'] = run_encrypt.get_encrypted()
        return True
    
    except Exception as e:
        print(f'ERROR: in func_encrypt \n{e}')
        return False

def func_decrypt(key, encrypted_data):
    try:
        run_decrypt = DECRYPT(key, encrypted_data)
        session['decrypted_data'] = run_decrypt.get_decrypted()
        return True
    except Exception as e:
        print(f'ERROR: in func_decrypt \n{e}')
        return False

if __name__ == '__main__':
    app.run(debug=True)
