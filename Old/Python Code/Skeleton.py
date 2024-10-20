import pandas as pd
import re

# Updated DataFrame with course availability and actual prerequisites
data = {
    'Course': ['CS110', 'CS122', 'CS210', 'CS211', 'CS212', 'CS313', 'CS314', 'CS330', 'CS415', 'CS425', 'MATH112',
               'MATH231', 'MATH232', 'MATH251', 'MATH252', 'MATH253'],
    'Course Name': ['Intro to CS', 'Intro to Programming', 'Systems Programming', 'Data Structures',
                    'Advanced Programming',
                    'Theory of Computation', 'Software Engineering', 'Algorithms', 'Database Systems',
                    'Machine Learning',
                    'Pre-Calculus', 'Linear Algebra', 'Calculus II', 'Calculus I', 'Calculus II', 'Calculus III'],
    'Prerequisites': [None, 'MATH101', 'MATH112Z', 'CS210', 'CS211', ['CS210', 'CS211', 'CS212', 'MATH231', 'MATH232'],
                      ['CS210', 'CS211', 'CS212'], 'CS314', 'CS330', 'CS315', None, 'MATH251', 'MATH231', 'MATH112Z',
                      'MATH251', 'MATH252'],
    'Offered Terms': [
        ['Fall'],  # CS110
        ['Fall', 'Winter'],  # CS122
        ['Fall'],  # CS210
        ['Winter'],  # CS211
        ['Spring'],  # CS212
        ['Fall'],  # CS313
        ['Winter'],  # CS314
        ['Spring'],  # CS330
        ['Fall'],  # CS415
        ['Winter'],  # CS425
        ['Fall', 'Winter'],  # MATH112
        ['Fall', 'Winter'],  # MATH231
        ['Spring'],  # MATH232
        ['Fall'],  # MATH251
        ['Spring', 'Winter'],  # MATH252
        ['Fall', 'Spring']  # MATH253
    ]
}

# Create the DataFrame
df = pd.DataFrame(data)

# Load the CSV file into a DataFrame
df_m = pd.read_csv('uo_courses_with_prerequisites.csv')


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
df_m['Credits'] = df_m['Course Name'].apply(extract_credits)

# Apply the function to clean up the "Prerequisites" column
df_m['Prerequisites'] = df_m['Prerequisites'].apply(clean_prerequisites)

# Split the "Course Code" into department and number, and clean the period
df_m[['Department', 'Course Number']] = df_m['Course Code'].apply(split_course_code)

# Select the relevant columns: "Department", "Course Number", "Credits", and the cleaned "Prerequisites" column
new_df = df_m[['Department', 'Course Number', 'Credits', 'Prerequisites']]

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
df_m = new_df[~(new_df["Credits"] == "No credits found")]
credits_col = df_m['Credits'].str.split(' ').str[0]
df_m.drop(columns="Credits")
df_m = df_m.reset_index().drop(columns="index")
df_m["Credits"] = credits_col
df_m["Course"] = df_m["Department"] + df_m["CourseNumber"].astype(str)


def clean_course_list(course_list):
    if course_list is None:
        return None
    # Remove non-breaking spaces and combine the subject and number
    return [course.replace('\xa0', '') for course in course_list]


df_m['Prerequisites'] = df_m['Prerequisites'].apply(clean_course_list)

# Display the cleaned dataframe
# print(df)

terms_data = [
    ("CS102", ["Fall", "Winter", "Spring"]),
    ("CS105", ["Spring"]),
    ("CS110", ["Fall", "Winter", "Spring"]),
    ("CS111", ["Fall", "Winter", "Spring"]),
    ("CS122", ["Fall", "Winter", "Spring"]),
    ("CS210", ["Fall", "Winter", "Spring"]),
    ("CS211", ["Winter", "Spring"]),
    ("CS212", ["Fall", "Spring"]),
    ("CS313", ["Fall", "Winter"]),
    ("CS314", ["Fall", "Winter"]),
    ("CS315", ["Winter", "Spring"]),
    ("CS322", ["Fall", "Spring"]),
    ("CS330", ["Winter", "Spring"]),
    ("CS332", ["Fall"]),
    ("CS333", ["Winter"]),
    ("CS372M", ["Winter"]),
    ("CS407", ["Fall", "Spring"]),
    ("CS415", ["Fall", "Spring"]),
    ("CS425", ["Fall", "Spring"]),
    ("CS407", ["Spring"]),
    ("CS507", ["Spring"]),
    ("CS410", ["Fall"]),
    ("CS510", ["Fall"]),
    ("CS422", ["Fall", "Winter", "Spring"]),
    ("CS522", ["Fall", "Winter", "Spring"]),
    ("CS423", ["Spring"]),
    ("CS523", ["Spring"]),
    ("CS429", ["Winter"]),
    ("CS529", ["Winter"]),
    ("CS431", ["Fall"]),
    ("CS531", ["Fall"]),
    ("CS432", ["Fall"]),
    ("CS532", ["Fall"]),
    ("CS433", ["Winter"]),
    ("CS533", ["Winter"]),
    ("CS434", ["Spring"]),
    ("CS534", ["Spring"]),
    ("CS436", ["Spring"]),
    ("CS536", ["Spring"]),
    ("CS437", ["Winter"]),
    ("CS537", ["Winter"]),
    ("CS441", ["Winter"]),
    ("CS541", ["Winter"]),
    ("CS443", ["Fall"]),
    ("CS543", ["Fall"]),
    ("CS445", ["Winter"]),
    ("CS545", ["Winter"]),
    ("CS451", ["Fall"]),
    ("CS551", ["Fall"]),
    ("CS453", ["Winter"]),
    ("CS553", ["Winter"]),
    ("CS471", ["Fall"]),
    ("CS571", ["Fall"]),
    ("CS472", ["Spring"]),
    ("CS572", ["Spring"]),
    ("CS473", ["Spring"]),
    ("CS573", ["Spring"]),
    ("CS610", ["Spring"]),
    ("CS621", ["Fall"]),
    ("CS630", ["Spring"]),
    ("CS631", ["Winter"]),
    ("CS633", ["Fall"]),
    ("CS640", ["Fall"]),
    ("CS670", ["Winter"]),
    ("CS607", ["Fall"]),
    ("CIT281", ["Spring"]),
    ("CIT381", ["Fall"]),
    ("CIT382", ["Winter"]),
    ("CIT383", ["Spring"]),
    ("MATH251", ["Fall", "Winter", "Spring"]),
    ("MATH252", ["Fall", "Winter", "Spring"]),
    ("MATH253", ["Fall", "Winter", "Spring"]),
]

terms = pd.DataFrame(terms_data, columns=["Course", "TermsOffered"])
df = df_m.merge(terms, on="Course", how="left")


def replace_float(value):
    # if isinstance(value, float):
    if True:
        return ["Fall", "Winter", "Spring"]
    else:
        return value

# Apply the function to the series
series_filled = df["TermsOffered"].apply(replace_float)
df["TermsOffered"] = series_filled

# for col in df.columns:
#     df[col] = df[col].apply(lambda x: ["Fall", "Winter", "Spring"] if x == "NaN" else x)

# print(df_merged)


# Dictionary containing majors and their required courses
major_requirements = {
    'Computer Science': ['CS210', 'CS211', 'CS212', 'CS313', 'CS314', 'CS330', 'CS415', 'CS425', 'MATH251', 'MATH252',
                         'MATH253'],
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


# Function to check if prerequisites are fulfilled
def prerequisites_fulfilled(course, courses_taken, df):
    prerequisites = find_prerequisites(course, df)
    return prerequisites.issubset(courses_taken)


# Function to build the four-year plan
def build_four_year_plan(major, starting_quarter='Fall', starting_year=2023):
    plan = {}
    courses_taken = {'MATH112Z', 'MATH 112', 'MATH101', 'MATH111', 'MATH 111', 'MATH112'}  # Start with an initial course for testing

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
            # print(sorted_courses)

            for course in sorted_courses:
                # Check if the course is available in the current term and if prerequisites are fulfilled
                row = df[df['Course'] == course]
                #print(row)
                if not row.empty and quarter in row.iloc[0]['TermsOffered']:
                    if course not in courses_taken and prerequisites_fulfilled(course, courses_taken, df) and len(
                            plan[f'Year {year + 1}'][term]) < 4:
                        plan[f'Year {year + 1}'][term].append(course)
                        courses_taken.add(course)
                        # print(f"DEBUG: Adding {course} to {term}")
                    # else:
                    # print(f"DEBUG: {course} prerequisites: {find_prerequisites(course, df)}, taken: {courses_taken}")

            # Increment year for the next quarter
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
