from flask import Flask, render_template, request
import pandas as pd
import re

app = Flask(__name__)

# Load the preprocessed DataFrame with course catalog
df = pd.read_csv('uo_courses_with_prerequisites.csv')

# Preprocessing functions (as per your original code)
def extract_credits(course_name):
    match = re.search(r'(\d+(-\d+)? Credits)', course_name)
    return match.group(1) if match else 'No credits found'

def clean_prerequisites(prereq):
    if pd.isna(prereq):
        return ''
    return re.sub(r'^(Prereq:|Requisites:)\s*', '', prereq)

def split_course_code(course_code):
    course_code = course_code.rstrip('.')
    match = re.match(r'([A-Z]+)\s*(\d+)', course_code)
    return pd.Series([match.group(1), match.group(2)]) if match else pd.Series([course_code, ''])

# Apply preprocessing steps to the DataFrame
df['Credits'] = df['Course Name'].apply(extract_credits)
df['Prerequisites'] = df['Prerequisites'].apply(clean_prerequisites)
df[['Department', 'CourseNumber']] = df['Course Code'].apply(split_course_code)
df['Course'] = df['Department'] + df['CourseNumber'].astype(str)

# Requirements for the CS major
cs_lower_division = ['CS 210', 'CS 211', 'CS 212', 'MATH 231', 'MATH 232']
cs_upper_division = ['CS 313', 'CS 314', 'CS 315', 'CS 330', 'CS 415', 'CS 422', 'CS 425']
math_requirements = ['MATH 251', 'MATH 252', 'MATH 253', 'MATH 341', 'MATH 343']
science_options = ['PHYS 201', 'PHYS 202', 'PHYS 203', 'CH 221', 'CH 222', 'CH 223', 'BI 211', 'BI 212', 'BI 213']
writing_requirement = ['WR 320', 'WR 321']

# Function to filter courses from the catalog dynamically based on the major requirements
def get_courses_for_requirement(requirement_courses):
    # Filter the DataFrame for matching course codes in the requirement list
    filtered_courses = df[df['Course'].isin(requirement_courses)]
    
    # Debug: Print filtered courses to see if they are being matched
    print(f"Filtered courses for requirement: {requirement_courses}")
    print(filtered_courses)
    
    return filtered_courses[['Department', 'CourseNumber', 'Credits', 'Prerequisites']]


# Function to group courses by term (Fall, Winter, Spring) and limit to 4 per term
def organize_courses_by_term(courses):
    terms = {
        'Fall 2024': [],
        'Winter 2025': [],
        'Spring 2025': []
    }
    
    # Loop over the courses and distribute them across terms
    for i, (_, row) in enumerate(courses.iterrows()):
        if len(terms['Fall 2024']) < 4:
            terms['Fall 2024'].append(row)
        elif len(terms['Winter 2025']) < 4:
            terms['Winter 2025'].append(row)
        elif len(terms['Spring 2025']) < 4:
            terms['Spring 2025'].append(row)

    return terms

@app.route('/', methods=['GET', 'POST'])
def index():
    cs_major_courses = {}
    terms = {}
    selected_major = None
    
    if request.method == 'POST':
        selected_major = request.form['major']
        if selected_major == 'CS':
            # Get the filtered CS major courses dynamically
            lower_division_core = get_courses_for_requirement(cs_lower_division)
            upper_division_core = get_courses_for_requirement(cs_upper_division)

            # Organize courses by terms and limit to 4 courses per term
            terms = organize_courses_by_term(pd.concat([lower_division_core, upper_division_core]))

    return render_template('index.html', major=selected_major, terms=terms)

if __name__ == '__main__':
    print(filtered_courses)

    app.run(debug=True, port=5002)
