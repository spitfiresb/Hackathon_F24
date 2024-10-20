# from flask import Flask, render_template, request
# import pandas as pd
# import re

# app = Flask(__name__)

# # Load the CSV file and preprocess it once
# df = pd.read_csv('uo_courses_with_prerequisites.csv')

# # Define a function to extract only the credits from the Course Name column
# def extract_credits(course_name):
#     match = re.search(r'(\d+(-\d+)? Credits)', course_name)
#     if match:
#         return match.group(1)
#     return 'No credits found'

# # Clean up the Prerequisites column
# def clean_prerequisites(prereq):
#     if pd.isna(prereq):
#         return ''
#     return re.sub(r'^(Prereq:|Requisites:)\s*', '', prereq)

# # Split course code into department and number
# def split_course_code(course_code):
#     course_code = course_code.rstrip('.')
#     match = re.match(r'([A-Z]+)\s*(\d+)', course_code)
#     if match:
#         return pd.Series([match.group(1), match.group(2)])
#     return pd.Series([course_code, ''])

# # Apply preprocessing steps
# df['Credits'] = df['Course Name'].apply(extract_credits)
# df['Prerequisites'] = df['Prerequisites'].apply(clean_prerequisites)
# df[['Department', 'Course Number']] = df['Course Code'].apply(split_course_code)

# # This is the preprocessed DataFrame
# new_df = df[['Department', 'Course Number', 'Credits', 'Prerequisites']]

# # Function to generate a grad plan based on the selected major
# def generate_grad_plan(major):
#     # Use the preprocessed DataFrame (new_df) to filter courses by major (department)
#     filtered_df = new_df[new_df['Department'] == major]
    
#     # Organize the courses by year and term (this logic can be adjusted as needed)
#     grad_plan = {
#         'Year 1': {'Fall': [], 'Winter': [], 'Spring': []},
#         'Year 2': {'Fall': [], 'Winter': [], 'Spring': []},
#         'Year 3': {'Fall': [], 'Winter': [], 'Spring': []},
#         'Year 4': {'Fall': [], 'Winter': [], 'Spring': []}
#     }

#     # Example logic for distributing courses across terms
#     for _, row in filtered_df.iterrows():
#         course_number = row['Course Number']
#         if '101' in course_number:
#             grad_plan['Year 1']['Fall'].append(f"{course_number} ({row['Credits']})")
#         elif '102' in course_number:
#             grad_plan['Year 1']['Winter'].append(f"{course_number} ({row['Credits']})")
#         elif '201' in course_number:
#             grad_plan['Year 2']['Fall'].append(f"{course_number} ({row['Credits']})")
#         # You can continue for other terms and years...

#     return grad_plan

# # Route for the home page
# @app.route('/', methods=['GET', 'POST'])
# def index():
#     grad_plan = None
#     selected_major = None
#     if request.method == 'POST':
#         selected_major = request.form['majors']
#         grad_plan = generate_grad_plan(selected_major)
    
#     return render_template('index.html', major=selected_major, grad_plan=grad_plan)

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load the preprocessed DataFrame containing the CS requirements
df = pd.read_csv('uo_courses_with_prerequisites.csv')

# Preprocess the DataFrame like you did earlier
# (Add the steps for splitting course codes, extracting credits, etc.)

# List of CS core courses
cs_core_courses = [
    'CS 210', 'CS 211', 'CS 212', 'CS 313', 'CS 314', 'CS 315', 'CS 330', 'CS 415', 'CS 422', 'CS 425'
]

# List of math courses
math_courses = ['MATH 231', 'MATH 232', 'MATH 251', 'MATH 252', 'MATH 253', 'MATH 341', 'MATH 343']

# List of science courses
science_courses = ['BI', 'CH', 'ERTH', 'PHYS']

# Function to generate the graduation plan
def generate_grad_plan(major):
    # Filter based on CS requirements subset
    cs_filtered = df[df['Course Code'].isin(cs_core_courses)]
    math_filtered = df[df['Course Code'].isin(math_courses)]
    science_filtered = df[df['Department'].isin(science_courses)]
    
    # Combine CS, Math, and Science courses
    grad_plan_courses = pd.concat([cs_filtered, math_filtered, science_filtered])

    # Organize the courses by year and term (simple logic here)
    grad_plan = {
        'Year 1': {'Fall': [], 'Winter': [], 'Spring': []},
        'Year 2': {'Fall': [], 'Winter': [], 'Spring': []},
        'Year 3': {'Fall': [], 'Winter': [], 'Spring': []},
        'Year 4': {'Fall': [], 'Winter': [], 'Spring': []}
    }

    # Distribute courses across terms (for demonstration, we'll keep it simple)
    for i, (index, row) in enumerate(grad_plan_courses.iterrows()):
        year = (i // 9) + 1  # Assign 9 courses per year
        if year > 4:
            break
        term = ['Fall', 'Winter', 'Spring'][i % 3]
        grad_plan[f'Year {year}'][term].append(f"{row['Course Code']} ({row['Credits']})")

    return grad_plan

# Route for the home page
@app.route('/', methods=['GET', 'POST'])
def index():
    grad_plan = None
    selected_major = None
    if request.method == 'POST':
        selected_major = request.form['majors']
        if selected_major == 'Computer Science':
            grad_plan = generate_grad_plan(selected_major)
    
    return render_template('index.html', major=selected_major, grad_plan=grad_plan)

if __name__ == '__main__':
    app.run(debug=True)

