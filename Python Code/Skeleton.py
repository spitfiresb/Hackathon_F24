import pandas as pd

# Sample DataFrame
data = {
    'Course': ['CS101', 'CS102', 'CS103', 'MATH101', 'MATH102', 'CS201', 'CS210', 'CS211', 'CS212'],
    'Code': ['101', '102', '103', '101', '102', '201', '210', '211', '212'],
    'Course Name': ['Intro to CS', 'Data Structures', 'Algorithms', 'Calculus I', 'Calculus II', 'Systems Programming', 'Advanced Topics in CS', 'Theory of Computation', 'Advanced Algorithms'],
    'Prerequisites': [None, 'CS101', 'CS102', 'MATH101', 'MATH101', 'CS103', ['MATH251', 'MATH252'], 'CS210', 'CS210']
}

df = pd.DataFrame(data)

def find_prerequisites(course, df, prereq_set):
    row = df[df['Course'] == course]
    if not row.empty and row.iloc[0]['Prerequisites']:
        prereqs = row.iloc[0]['Prerequisites']
        # Check if there are multiple prerequisites (a list)
        if isinstance(prereqs, list):
            for prereq in prereqs:
                if prereq not in prereq_set:
                    prereq_set.add(prereq)
                    # Recursively find the prerequisites of this prerequisite
                    find_prerequisites(prereq, df, prereq_set)
        else:
            # Single prerequisite case
            if prereqs not in prereq_set:
                prereq_set.add(prereqs)
                # Recursively find the prerequisites of this prerequisite
                find_prerequisites(prereqs, df, prereq_set)    

# Function to get all courses required for the major, including prerequisites
def get_courses_for_major(major_courses, df):
    required_courses = set(major_courses)
    prereq_set = set()
    
    for course in major_courses:
        find_prerequisites(course, df, prereq_set)
    
    # Combine the prerequisites with the original courses
    all_courses = required_courses.union(prereq_set)
    
    return all_courses

# Example: assuming these are the required courses for the major (e.g., Computer Science)
major_courses = ['CS211', 'CS212']

# Get the required courses, including prerequisites
required_courses = get_courses_for_major(major_courses, df)
print("Courses to take:", required_courses)