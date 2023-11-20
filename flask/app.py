from flask import Flask, jsonify, request
from extractor import GMAIL_EXTRACTOR
from extension_dt_model import DT_MODEL

app = Flask(__name__)
input_subject = 'Random'

@app.route('/api/subject', methods=['POST'])
def subject():
    # Get the data from the request
    data = request.get_json()

    # Access the value using the key 'data'
    input_subject = data.get('data', '')

    # Send a response back to the front-end
    return jsonify({'message': 'Data received successfully'})


@app.route('/api/ephishsense', methods=['GET'])
def main():
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
    
    return jsonify({'message': prediction})

if __name__ == '__main__':
    app.run(debug=True)
