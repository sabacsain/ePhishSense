
from flask import Flask, jsonify, request, session
from extractor import GMAIL_EXTRACTOR
from extension_dt_model import DT_MODEL
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:jenjen@localhost:3306/login'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'login-db'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Global variables
g_email = None
g_password = None
is_authenticated = False
input_subject = None

@app.route('/api/login', methods=['POST'])
def login():
    global g_email, g_password, is_authenticated
    is_authenticated = False

    try:
        # Get JSON data from the request body
        data = request.get_json()
        # print("Received data:", data)  # Debug print



        # Access emailInput and passInput from the JSON data
        email_input = data.get('email', '')
        pass_input = data.get('password', '')

        # print(f"Attempting to log in with email: {email_input}, password: {pass_input}")
        # user = User.query.filter_by(email=email_input).first()

        # if user:
        #     print(f"User found in DB: {user.email}")  # Debug print
        # else:
        #     print("No user found with that email.")  # Debug print

        # # Authenticate using the credentials
        user = User.query.filter_by(email=email_input).first()

        if user and pass_input == user.password:
            # Authentication is Successful
            is_authenticated = True

            # Transfer authenticated credentials to global variables
            g_email = email_input
            g_password = pass_input

            # Send a response back to the client
            return jsonify({'message': 'Login SUCCESSFUL'})
        else:
            return jsonify({'message': 'Login FAILED'})

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
    run = GMAIL_EXTRACTOR()
    input = run.value()

    predict = DT_MODEL(input)
    prediction = predict.result()

    # print(input)
    # print(prediction)
    
    return jsonify({'message': prediction})

if __name__ == '__main__':
    app.run(debug=True)
