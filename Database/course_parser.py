import pandas as pd
import re

# Load data from a CSV file
# Replace 'your_file.csv' with the actual path to your CSV file
df = pd.read_csv('your_file.csv', header=None)

# Function to extract prerequisites from DataFrame
def extract_prerequisites_from_df(df):
    prereqs_list = []
    
    for index, row in df.iterrows():
        # Use regex to find text after "Prereq:"
        match = re.search(r'Prereq:(.*?)\.?$', row[0])  # Assuming course info is in the first column
        if match:
            # Clean up and split the prerequisites
            prereq_str = match.group(1).strip()
            # Split by 'or' and clean spaces
            prereq_list = [prereq.strip() for prereq in re.split(r'\bor\b', prereq_str)]
            prereqs_list.append(prereq_list)
        else:
            prereqs_list.append([])  # Append an empty list if no prerequisites are found
            
    return prereqs_list

# Get the extracted prerequisites
prerequisites = extract_prerequisites_from_df(df)

# Create a new DataFrame with the course and its prerequisites
results_df = pd.DataFrame({
    'Course': df[0],  # Assuming the course info is in the first column
    'Prerequisites': ['; '.join(prereq) for prereq in prerequisites]  # Join lists into a single string
})

# Save the results to a new CSV file
results_df.to_csv('prerequisites_output.csv', index=False)

print("Prerequisites have been extracted and saved to 'prerequisites_output.csv'.")