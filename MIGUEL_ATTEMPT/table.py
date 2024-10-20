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
