import os, platform, pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score

# Get the OS 
which_os = platform.system()

# Perform forward/backward slash depending on the OS
slash = '\\' if which_os == 'Windows' else '/'

# Get the current directory
current_path = os.path.dirname(os.path.abspath(__file__))

# Concatenate directory path and dataset location
filepath = current_path + slash + 'new_dataset.csv'

# Load the dataset
df = pd.read_csv(filepath)

# Split the data into features and labels
X = df.drop('Label', axis=1)    # removes Label column then save to X dataframe
y = df['Label']                 # saves only the Label column then save to y dataframe

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

# Train the decision tree classifier
dt_model = DecisionTreeClassifier()
dt_model.fit(X_train.values, y_train.values)

# Make predictions on the test data
predictions = dt_model.predict(X_test.values)

# Calculate accuracy
accuracy = accuracy_score(y_test, predictions)
print(f'Accuracy: {accuracy}')

# Calculate precision
precision = precision_score(y_test, predictions)
print(f'Precision: {precision}')

# Calculate recall
recall = recall_score(y_test, predictions)
print(f'Recall: {recall}')

# Save the model to a file using pickle
save_path = current_path + slash + 'dt_model.pkl'
with open(save_path, 'wb') as model_file:
    pickle.dump(dt_model, model_file)

# Print the model path
print("Model: 'dt_model.pkl' has been saved.")
print(f"Saved at {save_path}")

