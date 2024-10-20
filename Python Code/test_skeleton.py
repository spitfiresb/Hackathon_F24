import pandas as pd
import re
from collections import defaultdict, deque
import networkx as nx


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

major_requirements = {
    'Computer Science': ['CS210', 'CS211', 'CS212', 'CS313', 'CS314', 'CS330', 'CS415', 'CS425', 'MATH251', 'MATH252',
                         'MATH253'],
}


def get_course_dependencies(df, required_courses, completed_courses=None):
    """Get course dependencies, marking completed courses as fulfilled."""
    if completed_courses is None:
        completed_courses = []

    prereq_map = defaultdict(list)
    term_map = defaultdict(list)
    indegree = defaultdict(int)  # Track the number of prerequisites for each course

    # Collect all prerequisites for the required courses
    for course in required_courses:
        course_info = df[df['Course'] == course]
        if not course_info.empty:
            prerequisites = course_info['Prerequisites'].values[0]
            terms = course_info['TermsOffered'].values[0]

            # Track course terms
            term_map[course] = terms

            # If prerequisites is None, treat it like no prerequisites
            if prerequisites is None:
                prerequisites = []

            # Track prerequisites and indegree
            for prereq in prerequisites:
                if prereq not in completed_courses:  # Skip already completed prerequisites
                    prereq_map[prereq].append(course)
                    indegree[course] += 1

    # Include courses with no prerequisites in the indegree map
    for course in required_courses:
        if course not in indegree:
            indegree[course] = 0

    return prereq_map, term_map, indegree


def topological_sort(prereq_map, indegree, completed_courses):
    """Topological sort adjusted to mark completed courses as visited."""
    # Kahn's Algorithm for topological sorting
    topo_order = []
    zero_indegree_queue = deque([course for course in indegree if indegree[course] == 0])

    # Start by adding all completed courses to the queue
    visited_courses = set(completed_courses)
    zero_indegree_queue.extend(completed_courses)  # Treat completed courses as ready to be scheduled

    while zero_indegree_queue:
        current_course = zero_indegree_queue.popleft()
        if current_course not in visited_courses:  # Skip already visited
            topo_order.append(current_course)
            visited_courses.add(current_course)

        # Decrease the indegree of the dependent courses
        for dependent in prereq_map[current_course]:
            indegree[dependent] -= 1
            if indegree[dependent] == 0:
                zero_indegree_queue.append(dependent)

    # If topological sorting does not visit all courses, a cycle exists
    if len(topo_order) != len(indegree) - len(completed_courses):  # Exclude completed courses
        unvisited_courses = set(indegree.keys()) - visited_courses
        raise ValueError(f"Cycle detected in prerequisites involving: {unvisited_courses}")

    return topo_order  # Valid topological sort


def expand_required_courses(df, required_courses):
    """ Expand the required courses to include all prerequisites. """
    expanded_courses = set(required_courses)
    prereq_map = defaultdict(list)

    # Build a quick prerequisite map from the dataframe
    for index, row in df.iterrows():
        course = row['Course']
        prerequisites = row['Prerequisites'] if row['Prerequisites'] else []
        for prereq in prerequisites:
            prereq_map[course].append(prereq)

    def add_prereqs(course):
        if course in prereq_map:
            for prereq in prereq_map[course]:
                if prereq not in expanded_courses:
                    expanded_courses.add(prereq)
                    add_prereqs(prereq)

    # For each required course, add its prerequisites recursively
    for course in required_courses:
        add_prereqs(course)

    return list(expanded_courses)


def check_for_cycles(df):
    """ Check the dataframe for cycles in the prerequisite graph. """
    G = nx.DiGraph()  # Create a directed graph

    for index, row in df.iterrows():
        course = row['Course']
        prerequisites = row['Prerequisites'] if row['Prerequisites'] else []
        for prereq in prerequisites:
            G.add_edge(prereq, course)  # Add directed edge from prerequisite to course

    # Detect cycles in the graph
    try:
        cycle = nx.find_cycle(G, orientation='original')
        if cycle:
            print(f"Cycle detected: {cycle}")
        else:
            print("No cycles detected.")
    except nx.exception.NetworkXNoCycle:
        print("No cycles detected.")


# Use the function to check for cycles
check_for_cycles(df)


# Main Execution with Completed Courses
completed_courses = ['MATH112']  # Example: MATH112 has already been completed
required_courses = ['CS210', 'CS313', 'WR320']
expanded_courses = expand_required_courses(df, required_courses)

prereq_map, term_map, indegree = get_course_dependencies(df, expanded_courses, completed_courses)

# Topologically sort courses
try:
    topo_order = topological_sort(prereq_map, indegree, completed_courses)
    # Generate the schedule based on the sorted courses
    schedule = generate_schedule(topo_order, term_map)

    # Output the schedule
    for year, terms in schedule.items():
        print(f"Year {year}:")
        for term, courses in terms.items():
            print(f"  {term}: {', '.join(courses)}")
except ValueError as e:
    print(e)

