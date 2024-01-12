import pandas as pd

# Load the CSV files into pandas DataFrames
file1 = '/home/sendoff/Music/csv-compare/new_dataset.csv'
file2 = '/home/sendoff/Music/csv-compare/final_dataset.csv'


# Read CSV files
df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)

# Drop the extra column from the DataFrame with extra column
extra_column_name = 'Email'  # Replace with the actual column name
df2 = df2.drop(columns=[extra_column_name], errors='ignore')

print(df2)
exit(0)

# Compare the DataFrames and find rows that are different
differences = df1.compare(df2)

# Display the rows with differences
print("Rows with differences:")
print(differences)
