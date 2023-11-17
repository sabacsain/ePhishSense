import pickle

# Load the model from the file
with open('dt_model.pkl', 'rb') as model_file:
    loaded_model = pickle.load(model_file)

# Code of Feature Extraction from EML file here

# Predict new input email
input_email = [1,1,1]       # random numeric value - phishing
predicted_label = loaded_model.predict([input_email])

# Print if malicious or non-malicious
if predicted_label == 0:
    print("Safe")
elif predicted_label == 1:
    print("Malicious")
else:
    print("System Error!")
