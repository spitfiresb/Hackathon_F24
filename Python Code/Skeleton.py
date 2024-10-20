import pandas as pd

# Updated DataFrame with course availability and actual prerequisites
data = {
    'Course': ['CS110', 'CS122', 'CS210', 'CS211', 'CS212', 'CS313', 'CS314', 'CS330', 'CS415', 'CS425', 'MATH112', 'MATH231', 'MATH232', 'MATH251', 'MATH252', 'MATH253'],
    'Course Name': ['Intro to CS', 'Intro to Programming', 'Systems Programming', 'Data Structures', 'Advanced Programming', 
                    'Theory of Computation', 'Software Engineering', 'Algorithms', 'Database Systems', 'Machine Learning',
                    'Pre-Calculus', 'Linear Algebra', 'Calculus II', 'Calculus I', 'Calculus II', 'Calculus III'],
    'Prerequisites': [None, 'MATH101', 'MATH112Z', 'CS210', 'CS211', ['CS210', 'CS211', 'CS212', 'MATH231', 'MATH232'],
                      ['CS210', 'CS211', 'CS212'], 'CS314', 'CS330', 'CS315', None, 'MATH251', 'MATH231', 'MATH112Z', 'MATH251', 'MATH252'],
    'Offered Terms': [
        ['Fall'],           # CS110
        ['Fall', 'Winter'], # CS122
        ['Fall'],           # CS210
        ['Winter'],         # CS211
        ['Spring'],         # CS212
        ['Fall'],           # CS313
        ['Winter'],         # CS314
        ['Spring'],         # CS330
        ['Fall'],           # CS415
        ['Winter'],         # CS425
        ['Fall', 'Winter'], # MATH112
        ['Fall', 'Winter'], # MATH231
        ['Spring'],         # MATH232
        ['Fall'],           # MATH251
        ['Spring', 'Winter'],         # MATH252
        ['Fall', 'Spring']            # MATH253
    ]
}

# Create the DataFrame
df = pd.DataFrame(data)

# Dictionary containing majors and their required courses
major_requirements = {
    'Computer Science': ['CS210', 'CS211', 'CS212', 'CS313', 'CS314', 'CS330', 'CS415', 'CS425', 'MATH251', 'MATH252', 'MATH253'],
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
    courses_taken = {'MATH112Z'}  # Start with an initial course for testing
    
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
                # Check if the course is available in the current term and if prerequisites are fulfilled
                row = df[df['Course'] == course]
                if not row.empty and quarter in row.iloc[0]['Offered Terms']:
                    if course not in courses_taken and prerequisites_fulfilled(course, courses_taken, df) and len(plan[f'Year {year + 1}'][term]) < 4:
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