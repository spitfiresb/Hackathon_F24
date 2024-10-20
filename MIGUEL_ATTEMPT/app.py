from flask import Flask, render_template, request
import pandas as pd
import re

app = Flask(__name__)

# Load the CSV file and preprocess it once
df = pd.read_csv('uo_courses_with_prerequisites.csv')

# Define a function to extract only the credits from the Course Name column
def extract_credits(course_name):
    match = re.search(r'(\d+(-\d+)? Credits)', course_name)
    if match:
        return match.group(1)
    return 'No credits found'

# Clean up the Prerequisites column
def clean_prerequisites(prereq):
    if pd.isna(prereq):
        return ''
    return re.sub(r'^(Prereq:|Requisites:)\s*', '', prereq)

# Split course code into department and number
def split_course_code(course_code):
    course_code = course_code.rstrip('.')
    match = re.match(r'([A-Z]+)\s*(\d+)', course_code)
    if match:
        return pd.Series([match.group(1), match.group(2)])
    return pd.Series([course_code, ''])

# Apply preprocessing steps
df['Credits'] = df['Course Name'].apply(extract_credits)
df['Prerequisites'] = df['Prerequisites'].apply(clean_prerequisites)
df[['Department', 'Course Number']] = df['Course Code'].apply(split_course_code)

# This is the preprocessed DataFrame
new_df = df[['Department', 'Course Number', 'Credits', 'Prerequisites']]

# Function to generate a grad plan based on the selected major
def generate_grad_plan(major):
    # Use the preprocessed DataFrame (new_df) to filter courses by major (department)
    filtered_df = new_df[new_df['Department'] == major]
    
    # Organize the courses by year and term (this logic can be adjusted as needed)
    grad_plan = {
        'Year 1': {'Fall': [], 'Winter': [], 'Spring': []},
        'Year 2': {'Fall': [], 'Winter': [], 'Spring': []},
        'Year 3': {'Fall': [], 'Winter': [], 'Spring': []},
        'Year 4': {'Fall': [], 'Winter': [], 'Spring': []}
    }

    # Example logic for distributing courses across terms
    for _, row in filtered_df.iterrows():
        course_number = row['Course Number']
        if '101' in course_number:
            grad_plan['Year 1']['Fall'].append(f"{course_number} ({row['Credits']})")
        elif '102' in course_number:
            grad_plan['Year 1']['Winter'].append(f"{course_number} ({row['Credits']})")
        elif '201' in course_number:
            grad_plan['Year 2']['Fall'].append(f"{course_number} ({row['Credits']})")
        # You can continue for other terms and years...

    return grad_plan

# Route for the home page
@app.route('/', methods=['GET', 'POST'])
def index():
    grad_plan = None
    selected_major = None
    if request.method == 'POST':
        selected_major = request.form['majors']
        grad_plan = generate_grad_plan(selected_major)
    
    return render_template('index.html', major=selected_major, grad_plan=grad_plan)

if __name__ == '__main__':
    app.run(debug=True)
