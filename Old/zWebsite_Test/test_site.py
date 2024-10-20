from pyscript import display

def show_selected_choices(major, year, science):
    # Call main function with provided parameters
    main(major, year, science)
    display(f"Selected Major: {major}", target="output")
    display(f"Selected Year: {year}", target="output")
    display(f"Selected Science Sequence: {science}", target="output")

def normalize_string(input: str) -> str:
    """Normalize the input string by stripping whitespace and converting to uppercase."""
    return input.strip().upper()

def eliminate_previous(courses: list[str], courses_taken: str) -> list[str]:
    """Eliminate courses that have been taken from the list."""
    taken_courses_list = [normalize_string(course) for course in courses_taken.split(",")]
    return [course for course in courses if normalize_string(course) not in taken_courses_list]

def build_term_schedule(cs_classes: list[str], mt_classes: list[str], sci_classes: list[str], current_year: int):
    """Output classes needed to take for each term based on what has been taken or not taken."""
    remaining_cs_classes = cs_classes[:]
    remaining_mt_classes = mt_classes[:]
    remaining_sci_classes = sci_classes[:]  # Add remaining science classes

    for year in range(current_year, 5):  # Generate schedules for years 1 to 4
        term_schedule = {
            "Fall": [],
            "Winter": [],
            "Spring": []
        }

        for term in term_schedule.keys():
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
            display(f"{term}: {classes}", target="output")

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

def cs_science_req(science_category):
    # Define science requirements similar to your original code
    # For brevity, I'm not including the full implementation here.
    return ['PHYS201', 'PHYS202']  # Placeholder return value

def main(major, year, science):
    cs_classes = ["CS122", "CS210", "CS211", "CS212", "CS313"]
    mt_classes = ["MATH231", "MATH232"]
    
    # Get the selected science classes based on the user's input
    selected_sci_classes = cs_science_req(science)

    # Simulate taken courses (you would collect this from user input in your UI)
    taken_cs_classes = ""  # You can replace with actual collected input
    taken_mt_classes = ""  # You can replace with actual collected input
    taken_sci_classes = ""  # You can replace with actual collected input

    remaining_cs_classes = eliminate_previous(cs_classes, taken_cs_classes)
    remaining_mt_classes = eliminate_previous(mt_classes, taken_mt_classes)
    remaining_sci_classes = eliminate_previous(selected_sci_classes, taken_sci_classes)

    current_year = get_year(year)
    build_term_schedule(remaining_cs_classes, remaining_mt_classes, remaining_sci_classes, current_year)

if __name__ == "__main__":
    pass  # Remove this to avoid running in a web context