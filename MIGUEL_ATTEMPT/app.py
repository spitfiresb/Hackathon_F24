import re
import random
from flask import Flask, render_template, request

app = Flask(__name__)

cs_classes = ["CS122", "CS210", "CS211", "CS212", "CS313", "CS314", "CS315", "CS330", "CS415", "CS422", "CS425"]
mt_classes = ["MATH231", "MATH232", "MATH251", "MATH252", "MATH253", "MATH341", "MATH342"]


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
def build_term_schedule(cs_classes: list[str], mt_classes: list[str], sci_classes: list[str], current_year: int) -> dict:
    """Output classes needed to take for each term based on what has been taken or not taken."""
    fall = ["CS102", "CS122", "CS210", "CS212", "CS313", "CS314", "CS322", "CS415", "CS425", "CS422", "CS431", "CS432", "CS443", "CS451", "CS471", "CS410", "DSCI311", "CS455", "CS413", "J431"]
    winter = ["CS102", "CS122", "CS210", "CS211", "CS313", "CS314", "CS315", "CS330", "CS333", "CS372M", "CS422", "CS429", "CS433", "CS445", "CS453", "CS410", "CS455", "CS413", "J431"]
    spring = ["CS102", "CS122", "CS210", "CS211", "CS212", "CS315", "CS322", "CS330", "CS415", "CS425", "CS422", "CS423", "CS434", "CS436", "CS472", "CS473", "CS410", "CS455", "CS413", "J431"]
    terms = {"Fall": fall, "Winter": winter, "Spring": spring}

    remaining_cs_classes = cs_classes[:]
    remaining_mt_classes = mt_classes[:]
    remaining_sci_classes = sci_classes[:]
    remaining_wr_classes = ["WR121", "WR123", "WR320"]
    remaining_gen_ed = ["A&L", "A&L", "A&L", "A&L", "SSC", "SSC", "SSC", "SSC", "GP", "US"]

    year = current_year
    schedule = {}

    while len(remaining_cs_classes) > 0 or len(remaining_mt_classes) > 0 or len(remaining_sci_classes) > 0 or len(remaining_wr_classes) > 0 or len(remaining_gen_ed) > 0:
        print(f"\nStarting year {year} with CS classes: {remaining_cs_classes}, MT classes: {remaining_mt_classes}, SCI classes: {remaining_sci_classes}")  # Debugging

        term_schedule = {
            "Fall": [],
            "Winter": [],
            "Spring": []
        }

        for term in term_schedule.keys():
            cs313_taken = "CS313" not in remaining_cs_classes
            max_cs_per_term = 2 if cs313_taken else 1
            cs_count = 0
            iter_cs = 0

            while cs_count < max_cs_per_term and iter_cs < len(remaining_cs_classes):
                selected_cs = remaining_cs_classes[iter_cs]
                if selected_cs in terms[term]:
                    print(f"Adding {selected_cs} to {term}")  # Debugging
                    term_schedule[term].append(selected_cs)
                    remaining_cs_classes.pop(iter_cs)
                    cs_count += 1
                else:
                    iter_cs += 1

            if remaining_mt_classes:
                term_schedule[term].append(remaining_mt_classes.pop(0))  # Assuming 1 MT class per term
            if remaining_sci_classes:
                term_schedule[term].append(remaining_sci_classes.pop(0))  # Assuming 1 SCI class per term

            while len(term_schedule[term]) < 4:
                if (len(remaining_wr_classes) > 0) and (year > 2):
                    term_schedule[term].append(remaining_wr_classes.pop(0))
                elif remaining_wr_classes:
                    if remaining_wr_classes[0] == "WR320":
                        pass
                    else:
                        term_schedule[term].append(remaining_wr_classes.pop(0))

                if remaining_gen_ed:
                    random_gened_course = random.choice(remaining_gen_ed)
                    remaining_gen_ed.remove(random_gened_course)
                    term_schedule[term].append(random_gened_course)
                break

        print(f"Year {year} Schedule: {term_schedule}")  # Debugging

        schedule[f"Year {year}"] = term_schedule
        year += 1
        if year >= 10:
            break

    return schedule
 # Return the complete schedule

def get_year(year: str) -> int:
    """Gets string of grade year and turns it into an int."""
    college_year = {
        "FRESHMAN": 1,
        "SOPHOMORE": 2,
        "JUNIOR": 3,
        "SENIOR": 4
    }

    normalized_year = normalize_string(year)
    if normalized_year not in college_year:
        return 0
    return college_year.get(normalized_year, 0)


def cs_science_req():
    cs_physics = [['PHYS201', 'PHYS202', 'PHYS203'],  # All 3 of these OR
                  ['PHYS251', 'PHYS252', 'PHYS253']]  # All 3 of these

    cs_chemistry = [['CH221', 'CH222', 'CH223'],  # All 3 of these OR
                    ['CH224H', 'CH225H', 'CH226H']]  # All 3 of these

    cs_geography = ['GEOG141', ['GEOG 321', 'GEOG322', 'GEOG323']]  # 2 from sublist

    cs_geological_sciences = ['ERTH201', 'ERTH202', 'ERTH203']  # All 3 of these

    cs_psycology = ['PSY201', ['PSY301', 'PSY304', 'PSY305', 'PSY348']]  # 2 from sublist

    cs_biology = [["BI211", "BI212", "BI213"],  # General Biology I,III,
                  ["CH111", "CH113", "CH221", "CH224H"],  # Or One of the following AND General Biology I-II
                  ["BI212", "BI213"]]

    science_category = (input(
        f"\nWhich science sequence are you taking? (Physics, Chemistry, Geography, Earth Science, Psychology, Biology): ")).upper()
    options = ['PHYSICS', 'CHEMISTRY', 'GEOGRAPHY', 'EARTH SCIENCE', 'PSYCHOLOGY', 'BIOLOGY']

    while not is_in_arr(science_category, options):
        print(f"{science_category} is not a valid major.")
        science_category = input(
            f"\nWhich science sequence are you taking? (Physics, Chemistry, Geography, Geological Sciences, Psychology, Biology): ").upper()

    match science_category:
        case 'PHYSICS':
            print(f'\nYou must take:\n\t(1) General Physics: {cs_physics[0]}\n\tOR \n\t(2) Foundations of Physics: {cs_physics[1]}')
            science_selection = input("Would you like the first or second option (Enter 1 OR 2): ")
            while (science_selection != '1') and (science_selection != '2'):
                print(f"\nInvalid input")
                science_selection = input("Would you like the first or second option (Enter 1 OR 2): ")
            return cs_physics[int(science_selection) - 1]

        case 'CHEMISTRY':
            print(f'\nYou must take:\n\t(1) General Chemistry: {cs_chemistry[0]}\n\tOR\n\t(2) Honors General Chemistry: {cs_chemistry[1]}')
            science_selection = input("Would you like the first or second option (Enter 1 OR 2): ")
            while (science_selection != '1') and (science_selection != '2'):
                print(f"\nInvalid input")
                science_selection = input("Would you like the first or second option (Enter 1 OR 2): ")
            return cs_chemistry[int(science_selection) - 1]

        case 'GEOGRAPHY':
            print(f'\nYou must take {cs_geography[0]} (The Natural Environment) and two classes from: {cs_geography[1]}')
            science_selection = (input(
                "Which of the two classes would you like to select (Enter TWO numbers separated by a comma: 1,2,3 ): "))
            science_selection = re.split(",\s*", science_selection)
            while (not all(elem in ['1', '2', '3'] for elem in science_selection)) or (len(science_selection) != 2) or (science_selection[0]==science_selection[1]):
                print(f"\nInvalid input")
                print(science_selection)
                science_selection = input(
                    "Which of the two classes would you like to select (Enter TWO numbers separated by a comma: 1,2,3 ): ")
                science_selection = re.split(",\s*", science_selection)
            class_list = ['GEOG141']
            for i in range(len(science_selection)):
                class_list.append(cs_geography[1][int(science_selection[i]) - 1])
            return class_list

        case 'EARTH SCIENCE':
            return cs_geological_sciences

        case 'PSYCHOLOGY':
            print(f'\nYou must take', cs_psycology[0], 'and two classes from:', cs_psycology[1])
            science_selection = (input(
                "Which of the two classes would you like to select (Enter TWO numbers separated by a comma: 1,2,3,4 ): ")).upper()
            science_selection = re.split(",\s*", science_selection)
            while (not all(elem in ['1', '2', '3'] for elem in science_selection)) or (len(science_selection) != 2) or (science_selection[0]==science_selection[1]):
                print(f"\nInvalid input")
                science_selection = input(
                    "Which of the two classes would you like to select (Enter TWO numbers separated by a comma: 1,2,3,4): ")
                science_selection = re.split(",\s*", science_selection)
            class_list = ['PSY201']
            for i in range(len(science_selection)):
                class_list.append(cs_psycology[1][int(science_selection[i]) - 1])
            return class_list

        case 'BIOLOGY':
            print(f'\nYou must take either:\n\t(1) General Biology I-III: {cs_biology[0]}\nOR\n\t(2) One of {cs_biology[1]} AND General Biology I-II {cs_biology[2]}')
            science_selection = input("Would you like the first or second option (Enter 1 OR 2): ")
            while (science_selection != '1') and (science_selection != '2'):
                print(f"\nInvalid input")
                science_selection = input("Would you like the first or second option (Enter 1 OR 2): ")
            if science_selection == '1':
                return cs_biology[0]
            else:
                class_list = []
                science_selection = input('Which class would you like to take from: CH111, CH113, CH221, CH224H (enter 1,2,3 or 4):')
                while (not all(elem in ['1', '2', '3', '4'] for elem in science_selection)) or (
                        len(science_selection) != 1):
                    print(f"\nInvalid input")
                    science_selection = input(
                        'Which class would you like to take from: CH111, CH113, CH221, CH224 (enter 1,2,3 or 4):')
                class_list.append(cs_biology[1][int(science_selection) - 1])
                class_list.append(cs_biology[2][0])
                class_list.append(cs_biology[2][1])
                return class_list


def cs_concentration_req():
    # High Performance Computing/Computational Science

    hpc = ["CS455",
           ["CS413", "CS429", "CS431", "CS445", "CS471"],  # Two of the following
           ["CS410", "CS410"]  # Two additional upper-level CS
           ]
    # Computer Networks
    networks = ["CS432",
                ["CS429", "CS433", "CS445"],  # Two of the following
                ["CS410", "CS410"]  # Two additional upper-level CS
                ]
    # Computer Security
    security = ["CS433",
                ["CS333", "CS432", "CS434", "CS436", "MATH458"],  # Two of the following
                ["CS410", "CS410"]  # Two additional upper-level CS
                ]
    # Machine Learning/AI/Data Science
    ai = ["CS472",
                ["DSCI311", "CS372M", "CS451", "CS453", "CS471", "CS473"],  # Two of the following
                ["CS410", "CS410"]  # Two additional upper-level CS
                ]
    # Software Development
    software_dev = [["CS423", "CS431", "CS436", "CS443", "CS445", "CS451", "CS461"],  # 3 of the following
                    ["CS410", "CS410"]  # Two additional upper-level CS
                    ]

    concentration = input("Which Concentration are you Taking? (HPC, Networks, Security, AI, Software): ").upper()
    options = ['HPC', 'NETWORKS', 'SECURITY', 'AI', 'SOFTWARE']
    while not is_in_arr(concentration, options):
        print(f"{concentration} is not a valid major.")
        concentration = input("Which Concentration are you Taking? (HPC, Networks, Security, AI, Software): ").upper()

    match concentration:

        case 'HPC':
            print(f"\nYou must take: \n\t{hpc[0]} (Computational Science) \nAND \n\tselect two classes from: {hpc[1]}\nAND \n\ttwo additional upper-level CS classes")
            selection = input("Which of the two classes would you like to select (Enter TWO numbers separated by a comma: 1,2,3,4,5): ")
            selection = re.split(",\s*", selection)
            while (not all(elem in ['1', '2', '3', '4', '5'] for elem in selection)) or (len(selection) != 2) or (selection[0]==selection[1]):
                print(f"\nInvalid input")
                selection = input("Which of the two classes would you like to select (Enter TWO numbers separated by a comma: 1,2,3,4,5): ")
                selection = re.split(",\s*", selection)
            return [hpc[0], hpc[1][int(selection[0]) - 1], hpc[1][int(selection[1]) - 1], hpc[2]]

        case 'NETWORKS':
            print(
                f"\nYou must take: \n\t{networks[0]} (Introduction to Computer Networks) \nAND \n\tselect two classes from: {networks[1]}\nAND \n\ttwo additional upper-level CS classes")
            selection = input(
                "Which of the two classes would you like to select (Enter TWO numbers separated by a comma: 1,2,3,4,5): ")
            selection = re.split(",\s*", selection)
            while (not all(elem in ['1', '2', '3', '4', '5'] for elem in selection)) or (len(selection) != 2) or (
                    selection[0] == selection[1]):
                print(f"\nInvalid input")
                selection = input(
                    "Which of the two classes would you like to select (Enter TWO numbers separated by a comma: 1,2,3,4,5): ")
                selection = re.split(",\s*", selection)
            return [networks[0], networks[1][int(selection[0]) - 1], networks[1][int(selection[1]) - 1], networks[2]]

        case 'SECURITY':
            print(
                f"\nYou must take: \n\t{security[0]} (Computer and Network Security) \nAND \n\tselect two classes from: {security[1]}\nAND \n\ttwo additional upper-level CS classes")
            selection = input(
                "Which of the two classes would you like to select (Enter TWO numbers separated by a comma: 1,2,3,4,5): ")
            selection = re.split(",\s*", selection)
            while (not all(elem in ['1', '2', '3', '4', '5'] for elem in selection)) or (len(selection) != 2) or (
                    selection[0] == selection[1]):
                print(f"\nInvalid input")
                selection = input(
                    "Which of the two classes would you like to select (Enter TWO numbers separated by a comma: 1,2,3,4,5): ")
                selection = re.split(",\s*", selection)
            # if '4' in the selection, add it to security[2] and return the other selection
            if '5' in selection:
                courses = ["CS102", "J431", security[0]]
                for i in range(len(selection)):
                    if selection[i] != '5':
                        courses.append(security[1][int(selection[i]) - 1])
                    else:
                        security[2].append(security[1][int(selection[i]) - 1])
                courses.append(security[2])
                return courses
            return ["CS102", "J431", security[0], security[1][int(selection[0]) - 1], security[1][int(selection[1]) - 1], security[2]]

        case 'AI':
            print(
                f"\nYou must take: \n\t{ai[0]} (Machine Learning) \nAND \n\tselect two classes from: {ai[1]}\nAND \n\ttwo additional upper-level CS classes")
            selection = input(
                "Which of the two classes would you like to select (Enter TWO numbers separated by a comma: 1,2,3,4,5,6): ")
            selection = re.split(",\s*", selection)
            while (not all(elem in ['1', '2', '3', '4', '5', '6'] for elem in selection)) or (len(selection) != 2) or (
                    selection[0] == selection[1]):
                print(f"\nInvalid input")
                selection = input(
                    "Which of the two classes would you like to select (Enter TWO numbers separated by a comma: 1,2,3,4,5,6): ")
                selection = re.split(",\s*", selection)
            return [ai[0], ai[1][int(selection[0]) - 1], ai[1][int(selection[1]) - 1], ai[2]]

        case 'SOFTWARE':
            print(
                f"\nYou must take three of the following: {software_dev[0]} \nAND \n\ttwo additional upper-level CS classes")
            selection = input(
                "Which of the three classes would you like to select (Enter THREE numbers separated by a comma: 1,2,3,4,5,6,7): ")
            selection = re.split(",\s*", selection)
            while (not all(elem in ['1', '2', '3', '4', '5', '6', '7'] for elem in selection)) or (len(selection) != 3) or (
                    selection[0] == selection[1]) or (selection[0] == selection[2]) or (selection[1] == selection[2]):
                print(f"\nInvalid input")
                selection = input(
                    "Which of the three classes would you like to select (Enter THREE numbers separated by a comma: 1,2,3,4,5,6,7): ")
                selection = re.split(",\s*", selection)
            return ["CS322", software_dev[0][int(selection[0]) - 1], software_dev[0][int(selection[1]) - 1], software_dev[0][int(selection[2]) - 1], software_dev[1]]

def main():
    cs_classes = ["CS122", "CS210", "CS211", "CS212", "CS313", "CS314", "CS315", "CS330", "CS415", "CS422",
                  "CS425"]
    mt_classes = ["MATH231", "MATH232", "MATH251", "MATH252", "MATH253", "MATH341", "MATH342"]
    upp_div_cs = []
    majors = [normalize_string(major) for major in ["Computer Science", "Data Science", "Business"]]  # Normalize majors

    input_major = input("What is Your Major?: ")
    normalized_major = normalize_string(input_major)  # Normalize the input major
    while not is_in_arr(normalized_major, majors):
        print(f"{input_major} is not a valid major.")
        input_major = input(f"\nWhat is Your Major? (e.g. Computer Science): ")
        normalized_major = normalize_string(input_major)

    input_year = input(f"\nWhat year are you in?: ")
    # Get the current year as an integer
    current_year = get_year(input_year)
    while current_year == 0:
        print(f"{input_year} is not a valid year.")
        input_year = input(f"\nWhat year are you in? (e.g. Freshman, Sophomore, Junior, Senior): ")
        current_year = get_year(input_year)

    # Get the selected science classes based on the user's input
    selected_sci_classes = cs_science_req()

    # Get the selected concentration classes based on the user's input
    selected_concentration_classes = cs_concentration_req()

    # Prompt for taken Science classes
    taken_sci_classes = input(
        f"\nIf you have taken any science sequence classes enter them here (separated by commas EX: PHYS201, PHYS202): ")
    remaining_sci_classes = eliminate_previous(selected_sci_classes, taken_sci_classes)

    # Prompt for taken CS classes
    taken_cs_classes = input(f"\nEnter CS classes you have taken (separated by commas): ")
    remaining_cs_classes = eliminate_previous(cs_classes, taken_cs_classes)

    # Prompt for taken Math classes
    taken_mt_classes = input(f"\nEnter Math classes you have taken (separated by commas): ")
    remaining_mt_classes = eliminate_previous(mt_classes, taken_mt_classes)

    remaining_upper_cs_classes = eliminate_previous(selected_concentration_classes[:-1], taken_cs_classes)
    remaining_cs_classes.extend(remaining_upper_cs_classes)
    remaining_upper_math_classes = eliminate_previous(selected_concentration_classes[-1], taken_mt_classes)
    remaining_mt_classes.extend(remaining_upper_math_classes)

    # Build and display the term schedule for the remaining years
    build_term_schedule(remaining_cs_classes, remaining_mt_classes, remaining_sci_classes, current_year)


# Route to render the form for user input
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        input_major = request.form.get("major")
        input_year = request.form.get("year")
        taken_sci_classes = request.form.get("sci_classes")
        taken_cs_classes = request.form.get("cs_classes")
        taken_mt_classes = request.form.get("mt_classes")

        normalized_major = normalize_string(input_major)
        current_year = get_year(input_year)

        selected_sci_classes = cs_science_req()
        selected_concentration_classes = cs_concentration_req()

        remaining_sci_classes = eliminate_previous(selected_sci_classes, taken_sci_classes)
        remaining_cs_classes = eliminate_previous(cs_classes, taken_cs_classes)
        remaining_mt_classes = eliminate_previous(mt_classes, taken_mt_classes)

        schedule = build_term_schedule(remaining_cs_classes, remaining_mt_classes, remaining_sci_classes, current_year)
        print(schedule) 
        return render_template("schedule.html", schedule=schedule)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
