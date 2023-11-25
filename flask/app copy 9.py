from flask import Flask, jsonify, request
from extractor import GMAIL_EXTRACTOR
from extension_dt_model import DT_MODEL
from login import LOGIN

app = Flask(__name__)

@app.route('/api/login', methods=['POST'])
def login():
    try:
        # Get JSON data from the request body
        data = request.get_json()

        # Access emailInput and passInput from the JSON data
        email_input = data.get('email', '')
        pass_input = data.get('password', '')

        # Authenticate using the credentials
        run = LOGIN(email_input, pass_input)

        if not (run.isAuthenticated()): 
            return jsonify({'message': 'Login FAILED'})

        # # For testing, print the values
        # print('Email Input:', email_input)
        # print('Password Input:', pass_input)

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
    global input_subject

    # Extract Email
    run = GMAIL_EXTRACTOR(input_subject)

    # Clear input subject
    input_subject = ''

    # Store numeric email value
    input = run.value()

    # Compare Email to the Model
    predict = DT_MODEL(input)
    prediction = predict.result()

    # print(input)
    # print(prediction)
    
    # Send the prediction to GUI
    return jsonify({'message': prediction})

if __name__ == '__main__':
    app.run(debug=True)
