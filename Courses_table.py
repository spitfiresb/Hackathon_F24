import pandas as pd
import re

# Load the CSV file into a DataFrame
df = pd.read_csv('uo_courses_with_prerequisites.csv')

# Define a function to extract only the credits from the Course Name column
def extract_credits(course_name):
    # Use regex to find the credits (assuming it's something like "4 Credits" or "1-5 Credits")
    match = re.search(r'(\d+(-\d+)? Credits)', course_name)
    if match:
        return match.group(1)  # Return only the matched credits part
    return 'No credits found'  # If no match, return a placeholder

# Define a function to clean up the "Prereq" or "Requisites" prefix in the Prerequisites column
def clean_prerequisites(prereq):
    if pd.isna(prereq):
        return ''
    # Use regex to remove the "Prereq:" or "Requisites:" prefix
    return re.sub(r'^(Prereq:|Requisites:)\s*', '', prereq)

# Apply the function to the "Course Name" column to create a new "Credits" column
df['Credits'] = df['Course Name'].apply(extract_credits)

# Apply the function to clean up the "Prerequisites" column
df['Prerequisites'] = df['Prerequisites'].apply(clean_prerequisites)

# Select the relevant columns: "Course Code", "Credits", and the cleaned "Prerequisites" column
new_df = df[['Course Code', 'Credits', 'Prerequisites']]

# Print the resulting DataFrame
print(new_df)
