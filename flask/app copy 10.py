from flask import Flask, jsonify, request
from extractor import GMAIL_EXTRACTOR
from extension_dt_model import DT_MODEL
from login import LOGIN
from encrypt import ENCRYPT
from decrypt import DECRYPT
import tempfile, os, imaplib

app = Flask(__name__)

# Initialize global variables
# is_authenticated = False
g_mail = None
key = ''
# temp_path = ''
encrypted_data = ''

@app.route('/api/login', methods=['POST'])
def login():
    global g_mail, key, encrypted_data
    print("origin")
    
    try:
        # Check if the user exists in the database
        # user = User.query.first()

        # if user:
        #     # print("norman")
        #     # User exists in the database, use credentials from the database
        #     g_email = user.email
        #     g_password = user.password

        #     print(g_email)
        #     print(g_password)
        # else:
            # print("norman2")
            # User does not exist in the database, authenticate using the provided credentials
            # Get JSON data from the request body
        data = request.get_json()

        # Access emailInput and passInput from the JSON data
        email_input = data.get('email', '')
        pass_input = data.get('password', '')

        run = LOGIN(email_input, pass_input)

        if not (run.isAuthenticated()):
            return jsonify({'message': 'Login FAILED'})

        # Get Mail Object
        g_mail = run.storeMail()

        print('BEFORE')
        run_encrypt = ENCRYPT(g_mail, email_input, pass_input)
        print('AFTER')
        # # Store mail object as string
        # connection_info = {
        # 'server': 'imap.gmail.com',
        # 'port': g_mail.port,
        # 'username': email_input,
        # 'password': pass_input
        # } 

        # str_g_mail = pickle.dumps(connection_info)

        # # Write mail object
        # run_encrypt = ENCRYPT(str_g_mail)

        # Get encryption key
        key = run_encrypt.get_key()
        # temp_path = run_encrypt.get_path()
        encrypted_data = run_encrypt.get_encrypted()


        print('norman1')

        # # Authentication is Successful
        # g_email = email_input
        # g_password = pass_input

        # Save the credentials to the database (assuming User is the model)
        # new_user = User(email=g_email)
        # new_user.set_password(g_password)  # Set the password using the set_password method
        # db.session.add(new_user)
        # db.session.commit()
        

        # Set authentication flag
        # is_authenticated = True

        # Clear data
        email_input = ''
        pass_input = '' 
        g_mail = ''

        # print(g_email)
        # print(g_password)
        # print(email_input)
        # print(pass_input)

        # Send a response back to the client
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

@app.route('/api/ephishsense', methods=['GET'])
def main():
    global input_subject, g_mail, key

    print("MAIN")
    run_decrypt = DECRYPT(key, encrypted_data)
    decrypted_data = run_decrypt.get_decrypted()

    g_mail = imaplib.IMAP4_SSL(decrypted_data['server'], decrypted_data['port'])
    print('norman')
    g_mail.login(decrypted_data['username'], decrypted_data['password'])

    # def read_from_temp_folder(temp_file_path):
    #     with open(temp_file_path, 'rb') as temp_file:
    #         data = temp_file.read()
    #     return data

    # g_mail = read_from_temp_folder(temp_path)

    print(g_mail)
    print("A-MAIN")

    # run_decrypt = DECRYPT(key, temp_path)
    # decrypted_g_mail = run_decrypt

    # print(decrypted_g_mail)
    # exit(0)

    ##decrypt

    if not g_mail:
        return jsonify({'message': 'Not Authenticated'})


    # Extract Email
    run = GMAIL_EXTRACTOR(input_subject, g_mail)

    # Clear data
    # input_subject = ''
    # g_email = ''
    # g_password = ''

    # Store numeric email value
    input = run.value()

    # Compare Email to the Model
    predict = DT_MODEL(input)
    prediction = predict.result()

    print(input)
    print(prediction)
    
    # Send the prediction to GUI
    return jsonify({'message': prediction})

    
    

if __name__ == '__main__':
    app.run(debug=True)
