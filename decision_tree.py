import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score, precision_score, recall_score

# Get the current directory
pwd = os.path.dirname(os.path.abspath(__file__))

# Concatenate directory path and dataset location
filepath = pwd + '/temp1.csv'

# Load the dataset
df = pd.read_csv(filepath)

# Split the data into features and labels
X = df.drop('Label', axis=1)    # removes Label column then save to X dataframe
y = df['Label']                 # saves only the Label column then save to y dataframe

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

# Train the decision tree classifier
clf = DecisionTreeClassifier()
clf.fit(X_train, y_train)

# Make predictions on the test data
predictions = clf.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, predictions)
print(f'Accuracy: {accuracy}')

# Calculate precision
precision = precision_score(y_test, predictions)
print(f'Precision: {precision}')

# Calculate recall
recall = recall_score(y_test, predictions)
print(f'Recall: {recall}')