import pandas as pd
import re

# Sample DataFrame with course availability and prerequisites
data = {
    'Course': ['CS110', 'CS122', 'CS210', 'CS211', 'CS212', 'CS313', 'CS314', 'CS322', 'CS330', 'CS415', 'CS420', 'CS425',
               'MATH112', 'MATH231', 'MATH232', 'MATH251', 'MATH252', 'MATH253'],
    'Code': ['110', '122', '210', '211', '212', '313', '314', '322', '330', '415', '420', '425',
             '112', '231', '232', '251', '252', '253'],
    'Course Name': ['Intro to CS', 'CS Fundamentals I', 'CS Fundamentals II', 'Intermediate CS I', 'Intermediate CS II',
                    'Data Structures', 'Algorithms', 'Software Engineering I', 'Operating Systems', 'Computer Networks',
                    'Database Systems', 'Machine Learning', 'Pre-Calculus II', 'Discrete Math I', 'Discrete Math II',
                    'Calculus I', 'Calculus II', 'Calculus III'],
    'Prerequisites': [None, 'MATH101', 'MATH112Z', 'CS210', 'CS211', ['CS210', 'CS211', 'CS212', 'MATH231', 'MATH232'],
                      ['CS210', 'CS211', 'CS212'], ['CS210', 'CS211', 'CS212'], 'CS314', 'CS330', 'CS315', 'CS315', 
                      'MATH111Z', 'MATH251', 'MATH231', 'MATH112Z', 'MATH251', 'MATH252'],
    'Offered Terms': [
        ['Fall', 'Winter'],  # CS110
        ['Fall', 'Winter'],  # CS122
        ['Fall', 'Winter'],  # CS210
        ['Winter'],          # CS211
        ['Spring'],          # CS212
        ['Winter'],          # CS313
        ['Spring'],          # CS314
        ['Winter', 'Spring'],# CS322
        ['Fall'],            # CS330
        ['Winter'],          # CS415
        ['Spring'],          # CS420
        ['Winter'],          # CS425
        ['Fall', 'Winter'],  # MATH112
        ['Winter'],          # MATH231
        ['Spring'],          # MATH232
        ['Fall'],            # MATH251
        ['Winter'],          # MATH252
        ['Spring']           # MATH253
    ]
}


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


def clean_course_list(course_list):
    if course_list is None:
        return None
    # Remove non-breaking spaces and combine the subject and number
    return [course.replace('\xa0', '') for course in course_list]


df['Prerequisites'] = df['Prerequisites'].apply(clean_course_list)


# Display the cleaned dataframe
print(df)

# Dictionary containing majors and their required courses
major_requirements = {
    'Computer Science': ['CS210', 'CS211', 'CS212', 'CS313', 'CS314', 'CS330', 'CS415', 'CS425'],
}

# Function to find prerequisites
def find_prerequisites(course, df, checked_courses=None):
    if checked_courses is None:
        checked_courses = set()

    if course in checked_courses:
        return set()

    checked_courses.add(course)
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
    
    quarter_mapping = ['Fall', 'Winter', 'Spring']
    
    for year in range(4):
        plan[f'Year {year + 1}'] = {}
        
        for quarter in quarter_mapping:
            term = f"{quarter} '{str(starting_year)[-2:]}"
            plan[f'Year {year + 1}'][term] = []
            
            major_courses = major_requirements.get(major, [])
            required_courses = get_courses_for_major(major_courses, df)
            
            sorted_courses = sorted(required_courses, key=lambda c: len(find_prerequisites(c, df)))

            for course in sorted_courses:
                row = df[df['Course'] == course]
                if not row.empty and quarter in row.iloc[0]['Offered Terms']:
                    if course not in courses_taken and len(plan[f'Year {year + 1}'][term]) < 4:
                        plan[f'Year {year + 1}'][term].append(course)
                        courses_taken.append(course)
            
            if quarter == 'Spring':
                starting_year += 1
    
    return plan

# Main function
def main():
    selected_major = input("Please enter your major (e.g., Computer Science): ")
    four_year_plan = build_four_year_plan(selected_major)
    
    for year, terms in four_year_plan.items():
        print(year)
        for term, courses in terms.items():
            print(f"{term} : {', '.join(courses) if courses else 'None'}")
        print()  # Blank line for readability

# Run the main function
if __name__ == "__main__":
    main()