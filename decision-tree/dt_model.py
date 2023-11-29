import os, platform, joblib

# Get the OS 
which_os = platform.system()

# Perform forward/backward slash depending on the OS
slash = '\\' if which_os == 'Windows' else '/'

# Get the current directory
current_path = os.path.dirname(os.path.abspath(__file__))

# Concatenate directory path and dataset location
filepath = current_path + slash + 'dt_model.joblib'

# Load the model from the file
loaded_model = joblib.load(filepath)

# Code of Feature Extraction from EML file here

# Predict new input email
input_email = [1,0,-1]       # random numeric value - phishing
predicted_label = loaded_model.predict([input_email])

# Print if malicious or non-malicious
if predicted_label == 0:
    print("Safe")
elif predicted_label == 1:
    print("Malicious")
else:
    print("System Error!")
