from flask import Flask, jsonify, request
from extractor import GMAIL_EXTRACTOR
from extension_dt_model import DT_MODEL
from login import LOGIN

app = Flask(__name__)

# Initialize global variables
is_authenticated = False
g_mail = None

@app.route('/api/login', methods=['POST'])
def login():
    global is_authenticated
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
        is_authenticated = True

        # Clear data
        email_input = ''
        pass_input = ''

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
    global input_subject, g_mail,  is_authenticated

    if not is_authenticated:
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
