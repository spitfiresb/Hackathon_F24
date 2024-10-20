def is_in_arr(input: str, our_arr: list[str]) -> bool:
    for elem in our_arr:
        if elem == input:
            return True
    return False
 
def normalize_string(input: str) -> str:
    """Normalize the input string by stripping whitespace and converting to uppercase."""
    return input.strip().upper()
 
def eliminate_previous(courses: list[str], courses_taken: str) -> list[str]:
    """Eliminate courses that have been taken and any lower-ranked courses from the list."""
    # Normalize the taken courses
    taken_courses_list = [normalize_string(course) for course in courses_taken.split(",")]
 
    # Find the highest index of taken courses
    max_index = -1
    for taken_course in taken_courses_list:
        if taken_course in courses:
            max_index = max(max_index, courses.index(taken_course))
 
    # Return only the courses that are at or above the highest taken course index
    return courses[max_index + 1:] if max_index != -1 else courses
 
def build_term_schedule(cs_classes: list[str], mt_classes: list[str], sci_classes: list[str], current_year: int):
    """Output classes needed to take for each term based on what has been taken or not taken."""
   
    # Create copies of the classes to modify them for each year
    remaining_cs_classes = cs_classes[:]
    remaining_mt_classes = mt_classes[:]
    remaining_sci_classes = sci_classes[:]  # Add remaining science classes
 
    # Iterate from the current year to the maximum year (4 for senior)
    for year in range(current_year, 5):  # Generate schedules for years 1 to 4
        print(f"\nYear {year} Schedule:")  # Display the correct year number
        term_schedule = {
            "Fall": [],
            "Winter": [],
            "Spring": []
        }
 
        for term in term_schedule.keys():
            # Ensure we only take one class from each category if available
            if remaining_cs_classes:
                selected_cs = remaining_cs_classes.pop(0)  # Add one CS class
                term_schedule[term].append(selected_cs)
            if remaining_mt_classes:
                selected_mt = remaining_mt_classes.pop(0)  # Add one Math class
                term_schedule[term].append(selected_mt)
            if remaining_sci_classes:
                selected_sci = remaining_sci_classes.pop(0)  # Add one Science class
                term_schedule[term].append(selected_sci)
 
        # Print the schedule for the current year
        for term, classes in term_schedule.items():
            print(f"{term}: {classes}")
 
def get_year(year: str) -> int:
    """Gets string of grade year and turns it into an int."""
    college_year = {
        "FRESHMAN": 1,
        "SOPHOMORE": 2,
        "JUNIOR": 3,
        "SENIOR": 4
    }
 
    normalized_year = normalize_string(year)
    return college_year.get(normalized_year, 0)
 
def cs_science_req():
    cs_physics = [['PHYS201', 'PHYS202', 'PHYS203'], # All 3 of these OR
                  ['PHYS251', 'PHYS252', 'PHYS253']] # All 3 of these
    
    cs_chemistry = [['CH221', 'CH222', 'CH223'],    # All 3 of these OR
                    ['CH224H', 'CH225H', 'CH226H']] # All 3 of these
    
    cs_geography = ['GEOG141', ['GEOG 321', 'GEOG322', 'GEOG323']] # 2 from sublist

    cs_geological_sciences = [['ERTH201', 'ERTH202', 'ERTH203'], # All 3 of these OR
                              ['GEOL201', 'GEOL202', 'GEOL203']] # All 3 of these
    
    cs_psycology = ['PSY201', ['PSY301', 'PSY304', 'PSY305', 'PSY348']] # 2 from sublist

    cs_biology = [['CH111', 'CH113', 'CH221', 'CH224'], 'BI211', ['BI212', 'BI213']] # 1 from first sublist, 1 from second sublist

    science_category = (input("Which science sequence are you taking? (Physics, Chemistry, Geography, Geological Sciences, Psychology, Biology): ")).upper()
    options = ['PHYSICS', 'CHEMISTRY', 'GEOGRAPHY', 'GEOLOGICAL SCIENCES', 'PSYCOLOGY', 'BIOLOGY']
    if is_in_arr(science_category, options):
        print(f"{science_category} is a valid major.")
    else:
        print(f"{science_category} is not a valid major.")
        return cs_science_req()
        
    if science_category == 'PHYSICS':
        print('You must take', cs_physics[0], 'OR', cs_physics[1])
        science_selection = (input("Would you like the first or second option (Enter 1 OR 2): ")).upper()
        print(science_selection)
        if science_selection != '1' and science_selection != '2':
            return cs_science_req()
        else: return cs_physics[int(science_selection) - 1]

    if science_category == 'CHEMISTRY':
        print('You must take', cs_chemistry[0], 'OR', cs_chemistry[1])
        science_selection = (input("Would you like the first or second option (Enter 1 OR 2): ")).upper()
        if science_selection != '1' and science_selection != '2':
            return cs_science_req()
        else: return cs_chemistry[int(science_selection) - 1]

    if science_category == 'GEOGRAPHY':
        print('You must take', cs_geography[0], 'and two classes from:', cs_geography[1])
        science_selection = (input("Which of the two classes would you like to select (Enter TWO numbers separated by a comma: 1,2,3 ): ")).upper()
        science_selection = science_selection.split(",")
        class_list = ['GEOG141']
        for i in range(len(science_selection)):
            class_list.append(cs_geography[1][int(science_selection[i]) - 1])
        return class_list

    if science_category == 'GEOLOGICAL SCIENCES':
        print('You must take', cs_geological_sciences[0], 'OR', cs_geological_sciences[1])
        science_selection = (input("Would you like the first or second option (Enter 1 OR 2): ")).upper()
        if science_selection != '1' and science_selection != '2':
            return cs_science_req()
        else: return cs_geological_sciences[int(science_selection) - 1]

    if science_category == 'PSYCOLOGY':
        print('You must take', cs_psycology[0], 'and two classes from:', cs_psycology[1])
        science_selection = (input("Which of the two classes would you like to select (Enter TWO numbers separated by a comma: 1,2,3,4 ): ")).upper()
        science_selection = science_selection.split(",")
        class_list = ['PSY201']
        for i in range(len(science_selection)):
            class_list.append(cs_psycology[1][int(science_selection[i]) - 1])
        return class_list
    
    if science_category == 'BIOLOGY':
        print('You must take one of:', cs_biology[0],',', cs_biology[1],'and one of:', cs_biology[2])
        class_list = []
        science_selection = (input('Which class would you like to take from: CH111, CH113, CH221, CH224 (enter 1,2,3 or 4):' )).upper()
        if len(science_selection) > 1:
            print("Invalid input")
            return cs_science_req()
        class_list.append(cs_biology[0][int(science_selection) - 1])
        class_list.append(cs_biology[1])
        science_selection = (input('Which class would you like to take from: BI212, BI213 (enter 1 or 2):' )).upper()
        if len(science_selection) > 1:
            print("Invalid input")
            return cs_science_req()
        class_list.append(cs_biology[2][int(science_selection) - 1])
        return class_list
 
def main():
    cs_classes = ["CS122", "CS210", "CS211", "CS212", "CS313", "CS314", "CS315", "CS330", "CS415", "CS415", "CS422", "CS425"]
    mt_classes = ["MATH231", "MATH232", "MATH251", "MATH252", "MATH253", "MATH341", "MATH342"]
    upp_div_cs = []
    majors = [normalize_string(major) for major in ["Computer Science", "Data Science", "Business"]]  # Normalize majors
   
 
    input_major = input("What is your major: ")
    input_year = input("What year are you in?: ")
    normalized_major = normalize_string(input_major)  # Normalize the input major
    if is_in_arr(normalized_major, majors):
        print(f"{input_major} is a valid major.")
    else:
        print(f"{input_major} is not a valid major.")
        return  # Exiting if major is invalid
 
    # Get the selected science classes based on the user's input
    selected_sci_classes = cs_science_req()
 
    # Prompt for taken Science classes
    taken_sci_classes = input("If you have taken any science sequence classes enter them here (separated by commas EX: PHYS201, PHYS202): ")
    remaining_sci_classes = eliminate_previous(selected_sci_classes, taken_sci_classes)
 
    # Prompt for taken CS classes
    taken_cs_classes = input("Enter CS classes you have taken (separated by commas): ")
    remaining_cs_classes = eliminate_previous(cs_classes, taken_cs_classes)
 
    # Prompt for taken Math classes
    taken_mt_classes = input("Enter Math classes you have taken (separated by commas): ")
    remaining_mt_classes = eliminate_previous(mt_classes, taken_mt_classes)
 
    # Get the current year as an integer
    current_year = get_year(input_year)
 
    # Build and display the term schedule for the remaining years
    build_term_schedule(remaining_cs_classes, remaining_mt_classes, remaining_sci_classes, current_year)
 
if __name__ == "__main__":
    main()
 