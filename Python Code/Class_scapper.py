import requests
from bs4 import BeautifulSoup
import csv

# Base URL of the University of Oregon course catalog
base_url = 'https://catalog.uoregon.edu/courses/'

# List of department codes to scrape
departments = ['AEIS', 'ACTG', 'AFR', 'ASL', 'ANTH', 'ARB', 'ARCH', 'ART', 'ARH', 'ARTD', 'ARTC', 'ARTF', 'ARTM', 'ARTP', 'ARTO', 'ARTR', 'ARTS', 'ASIA', 'ASTR', 'BEHT', 'BIOE', 'BI', 'BLST', 'BRIN', 'BA', 'BE', 'CH', 'CHN', 'CINE', 'CLAS', 'CAS', 'DSGN', 'CDS', 'COLT', 'CIT', 'CS', 'CRES', 'CPSY', 'CFT', 'CRWR', 'DANC', 'DAN', 'DANE', 'DSCI', 'ERTH', 'EALL', 'EC', 'EDUC', 'EDST', 'EDLD', 'ENG', 'ENVD', 'ENVS', 'ES', 'EURO', 'FHS', 'FIN', 'FLR', 'FR', 'GEOG', 'GER', 'GLBL', 'GSL', 'GRST', 'GRK', 'HBRW', 'AAAP', 'HIST', 'HC', 'HPHY', 'HUM', 'ICH', 'IST', 'IARC', 'ITAL', 'JPN', 'JCOM', 'JDST', 'KRN', 'LERC', 'LA', 'LT', 'LAT', 'LAS', 'LAW', 'LIB', 'LING', 'MGMT', 'MKTG', 'MATH', 'MDVL', 'MENA', 'MIL', 'ANTM', 'MUS', 'MUE', 'MUJ', 'MUP', 'OBA', 'PHIL', 'PHYS', 'PPPM', 'PS', 'PORT', 'PREV', 'PD', 'PSY', 'REL', 'RL', 'RUSS', 'REES', 'SCAN', 'SPSY', 'SOC', 'SPAN', 'SPED', 'SBUS', 'SPD', 'SPM', 'STAT', 'SWAH', 'SWED', 'TA', 'UGST', 'WGS', 'WR']

# Function to scrape courses from a department page
def scrape_department(dept_code):
    url = f'{base_url}crs-{dept_code.lower()}/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    courses = []

    # Find all course blocks
    course_blocks = soup.find_all('div', class_='courseblock')
    for block in course_blocks:
        # Extract course code and name
        title = block.find('p', class_='courseblocktitle').get_text(strip=True)
        course_code, course_name = title.split(' ', 1)

        # Extract course description
        description = block.find('p', class_='courseblockdesc').get_text(strip=True)

        # Extract prerequisites
        prereqs = block.find('p', class_='courseblockprereq')
        prerequisites = prereqs.get_text(strip=True) if prereqs else 'None'

        courses.append([course_code, course_name, description, prerequisites])
    return courses

# CSV file to save the course data
with open('uo_courses.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write header row
    writer.writerow(['Course Code', 'Course Name', 'Description', 'Prerequisites'])

    # Scrape each department and write to CSV
    for dept in departments:
        dept_courses = scrape_department(dept)
        writer.writerows(dept_courses)

print("Course data extraction completed. Check 'uo_courses.csv' for the compiled list.")
