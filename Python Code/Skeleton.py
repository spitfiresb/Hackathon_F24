import pandas as pd
import re

"""
This script generates a four-year course plan for a selected major based on its required courses and prerequisites. 
It reads course data from a pandas DataFrame and constructs a list of classes, ensuring that prerequisites are fulfilled 
before advanced courses. The user selects their major, and the script outputs a term-by-term schedule over four academic 
years starting from a given year and quarter.
"""

# Sample DataFrame with course availability
data = {
    'Course': ['CS122', 'CS102', 'CS103', 'MATH101', 'MATH102', 'CS201', 'CS210', 'CS211', 'CS212',
               'CS300', 'CS301', 'CS302', 'MATH251', 'MATH252', 'MATH253', 'CS401', 'CS402'],
    'Code': ['101', '102', '103', '201', '202', '301', '302', '401', '402', 
             '501', '502', '503', '601', '602', '603', '701', '702'],
    'Course Name': ['Intro to CS', 'Data Structures', 'Algorithms', 'Calculus I', 'Calculus II',
                    'Systems Programming', 'Advanced Topics in CS', 'Theory of Computation', 
                    'Advanced Algorithms', 'Software Engineering', 'Database Systems', 
                    'Machine Learning', 'Discrete Math', 'Linear Algebra', 'Statistics',
                    'Capstone Project', 'Computer Networks'],
    'Prerequisites': [None, 'CS122', 'CS102', 'MATH101', 'MATH101', 'CS103', 
                     ['MATH251', 'MATH252'], 'CS210', 'CS211', 
                     'CS212', 'CS302', 'MATH101', 'MATH102', 
                     'MATH251', 'MATH252', ['CS401', 'CS402'], 'CS301'],
    'Offered Terms': [
        ['Fall', 'Winter'],  # CS122
        ['Fall', 'Spring'],  # CS102
        ['Winter'],          # CS103
        ['Fall'],            # MATH101
        ['Winter', 'Spring'], # MATH102
        ['Fall'],            # CS201
        ['Fall'],            # CS210
        ['Winter'],          # CS211
        ['Spring'],          # CS212
        ['Fall'],            # CS300
        ['Fall', 'Winter'],  # CS301
        ['Winter', 'Spring'], # CS302
        ['Fall'],            # MATH251
        ['Spring'],          # MATH252
        ['Fall', 'Spring'],  # MATH253
        ['Fall'],            # CS401
        ['Winter']           # CS402
    ]
}


# Load the CSV file into a DataFrame
df = pd.read_csv('../Database/uo_courses_with_prerequisites.csv')


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


def split_course_code(course_code):
    # Remove period at the end, if any
    course_code = course_code.rstrip('.')
    # Split the course code into department and number
    match = re.match(r'([A-Z]+)\s*(\d+)', course_code)
    if match:
        return pd.Series([match.group(1), match.group(2)])
    return pd.Series([course_code, ''])  # Return original if no match


# Apply the function to the "Course Name" column to create a new "Credits" column
df['Credits'] = df['Course Name'].apply(extract_credits)

# Apply the function to clean up the "Prerequisites" column
df['Prerequisites'] = df['Prerequisites'].apply(clean_prerequisites)

# Split the "Course Code" into department and number, and clean the period
df[['Department', 'Course Number']] = df['Course Code'].apply(split_course_code)

# Select the relevant columns: "Department", "Course Number", "Credits", and the cleaned "Prerequisites" column
new_df = df[['Department', 'Course Number', 'Credits', 'Prerequisites']]

# Print the resulting DataFrame
new_df = new_df.rename(columns={"Course Number": "CourseNumber"})
new_df["CourseNumber"] = new_df["CourseNumber"].astype(int)


# Define the function to clean and extract course codes (e.g., "CS 210")
def clean_prerequisites(prereq):
    if pd.isna(prereq):
        return None
    # Extract course codes (e.g., "CS 210") using regex pattern for course codes (letters followed by numbers)
    courses = re.findall(r'[A-Z]+\s*\d{3}', prereq)
    if len(courses) == 0:
        return None
    return courses


# Apply the function to clean the 'Prerequisites' column
new_df['Prerequisites'] = new_df['Prerequisites'].apply(clean_prerequisites)

# # Step 1: Ensure 'Credits' is treated as a string and handle any non-string values
new_df['Credits'] = new_df['Credits'].astype(str)  # Convert to string first to handle NaN values
df = new_df[~(new_df["Credits"] == "No credits found")]
credits_col = df['Credits'].str.split(' ').str[0]
df.drop(columns="Credits")
df = df.reset_index().drop(columns="index")
df["Credits"] = credits_col
df["Course"] = df["Department"] + df["CourseNumber"].astype(str)

# Display the cleaned dataframe
print(df)

# Dictionary containing majors and their required courses
major_requirements = {
    'Computer Science': ['CS211', 'CS212', 'CS301', 'CS302', 'CS401', 'CS402'],
}

# Function to find prerequisites
def find_prerequisites(course, df, checked_courses=None):
    if checked_courses is None:
        checked_courses = set()  # Initialize the checked_courses set on the first call

    # Avoid infinite recursion
    if course in checked_courses:
        return set()  # Return an empty set if this course has already been checked

    checked_courses.add(course)  # Mark this course as checked
    prereqs = set()
    
    row = df[df['Course'] == course]
    if not row.empty and row.iloc[0]['Prerequisites']:
        prerequisites = row.iloc[0]['Prerequisites']
        if isinstance(prerequisites, list):
            for prereq in prerequisites:
                prereqs.add(prereq)
                prereqs.update(find_prerequisites(prereq, df, checked_courses))
        else:
            prereqs.add(prerequisites)
            prereqs.update(find_prerequisites(prerequisites, df, checked_courses))
    
    return prereqs

# Function to get courses for major
def get_courses_for_major(major_courses, df):
    required_courses = set(major_courses)
    prereq_set = set()
    
    for course in major_courses:
        prereq_set.update(find_prerequisites(course, df))
    
    all_courses = required_courses.union(prereq_set)
    return all_courses

# Function to build the four-year plan
def build_four_year_plan(major, starting_quarter='Fall', starting_year=2023):
    plan = {}
    courses_taken = []
    
    # Create a mapping of quarter to index for easy reference
    quarter_mapping = ['Fall', 'Winter', 'Spring']
    
    for year in range(4):
        plan[f'Year {year + 1}'] = {}
        
        for quarter in quarter_mapping:
            term = f"{quarter} '{str(starting_year)[-2:]}"
            plan[f'Year {year + 1}'][term] = []
            
            major_courses = major_requirements.get(major, [])
            required_courses = get_courses_for_major(major_courses, df)
            
            # Sort the courses by the number of prerequisites (ascending)
            sorted_courses = sorted(required_courses, key=lambda c: len(find_prerequisites(c, df)))

            for course in sorted_courses:
                # Check if the course is available in the current term
                row = df[df['Course'] == course]
                if not row.empty and quarter in row.iloc[0]['Offered Terms']:
                    if course not in courses_taken and len(plan[f'Year {year + 1}'][term]) < 4:
                        plan[f'Year {year + 1}'][term].append(course)
                        courses_taken.append(course)
            
            # Increment year for the next quarter
            if quarter == 'Spring':
                starting_year += 1
    
    return plan

# Main function
def main():
    selected_major = input("Please enter your major (e.g., Computer Science): ") #TODO this input needs to come from HTML!!
    four_year_plan = build_four_year_plan(selected_major)
    
    for year, terms in four_year_plan.items():
        print(year)
        for term, courses in terms.items():
            print(f"{term} : {', '.join(courses) if courses else 'None'}")
        print()  # Blank line for readability

# Run the main function
if __name__ == "__main__":
    main()