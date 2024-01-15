import os, platform, pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix

# Get the OS 
which_os = platform.system()

# Perform forward/backward slash depending on the OS
slash = '\\' if which_os == 'Windows' else '/'

# Get the current directory
current_path = os.path.dirname(os.path.abspath(__file__))

# Concatenate directory path and dataset location
filepath = current_path + slash + 'final_dataset.csv'

# Load the dataset
df = pd.read_csv(filepath)

# Split the data into features and labels
X = df.drop(['Label', 'Email'], axis=1)    # removes Label column then save to X dataframe
# X = df.drop('Label', axis=1)    # removes Label column then save to X dataframe
y = df['Label']                 # saves only the Label column then save to y dataframe

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

# Train the decision tree classifier
dt_model = DecisionTreeClassifier()
dt_model.fit(X_train.values, y_train.values)

# Make predictions on the test data
predictions = dt_model.predict(X_test.values)


##################################################################
# CALCULATING PERFORMANCE MATRIX
##################################################################

# Calculate accuracy
accuracy = accuracy_score(y_test, predictions)
print(f'Accuracy: {accuracy}')

# Calculate precision
precision = precision_score(y_test, predictions)
print(f'Precision: {precision}')

# Calculate recall
recall = recall_score(y_test, predictions)
print(f'Recall: {recall}')

# Create a confusion matrix
conf_matrix = confusion_matrix(y_test, predictions)

# Extract True Negative (TN), True Positive (TP), False Negative (FN), False Positive (FP)
tn, fp, fn, tp = conf_matrix.ravel()

print(f"True Positive: {tp}")
print(f"True Negative: {tn}")
print(f"False Positive: {fp}")
print(f"False Negative: {fn}")


##################################################################
# EXPORTING TESTING DATASET
##################################################################

# # Create DataFrames for the training and testing sets
# train_df = pd.concat([X_train, y_train], axis=1)

# # Add the 'text_column' back to the test_df
# test_df = pd.concat([X_test, y_test, df.loc[X_test.index]['Email']], axis=1)

# # Export the training and testing sets to separate CSV files
# train_df.to_csv(current_path + slash + 'training_data.csv', index=False)
# test_df.to_csv(current_path + slash + 'testing_data.csv', index=False)

# Create a DataFrame with the specified columns
result_df = pd.DataFrame({
    'ID': range(1, len(X_test) + 1),
    'Email': df.loc[X_test.index, 'Email'],
    'Actual Label': y_test,
    'Predicted Label': predictions,
    'Evaluation': ['TP' if actual == 1 and predicted == 1 else
                'TN' if actual == 0 and predicted == 0 else 
                'FP' if actual == 0 and predicted == 1 else 
                'FN' if actual == 1 and predicted == 0 else 
                'Error' 
                for actual, predicted in zip(y_test, predictions)]
})

# Export the DataFrame to a CSV file
result_df.to_csv(current_path + slash + 'testing_data.csv', index=False)


# # Create a DataFrame with the specified columns
# result_df = pd.DataFrame({
#     'ID': range(1, len(X_test) + 1),
#     'Actual Label': y_test,
#     'Predicted Label': predictions,
#     'Evaluation': ['TP' if actual == 1 and predicted == 1 else
#                     'TN' if actual == 0 and predicted == 0 else 
#                     'FP' if actual == 0 and predicted == 1 else 
#                     'FN' if actual == 1 and predicted == 0 else 
#                     'Error' 
#                     for actual, predicted in zip(y_test, predictions)]
# })

# # Export the DataFrame to a CSV file
# result_df.to_csv(current_path + slash + 'testing_data.csv', index=False)



##################################################################
# EXPORTING THE DECISION TREE MODEL
##################################################################

# # Save the model to a file using pickle
# save_path = current_path + slash + 'dt_model.pkl'
# with open(save_path, 'wb') as model_file:
#     pickle.dump(dt_model, model_file)

# # Print the model path
# print("Model: 'dt_model.pkl' has been saved.")
# print(f"Saved at {save_path}")

