from flask import Flask, jsonify
from extractor import GMAIL_EXTRACTOR
from extension_dt_model import DT_MODEL

app = Flask(__name__)

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
