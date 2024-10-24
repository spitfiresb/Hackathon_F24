
# Degree Scheduler

## Overview

This is a project made by me and my group members during the Fall 2024 University of Oregon Hackathon. Included in this repository is all the files that were created throughout the process, showcasing our entire workflow. 

The Degree Scheduler project is designed to help university students plan and manage their four-year course schedules effectively. The program utilizes course prerequisite data and scheduling logic to assist students in selecting the right courses for each term, while ensuring that they meet all major requirements. 

This project is especially useful for students following a structured academic program, like Computer Science or Data Science, as it can generate customized schedules based on prerequisites and course availability.

## Features

- **Course Management**: Manages a list of courses and tracks which have been taken.
- **Prerequisite Handling**: Ensures that students can only register for courses that meet the prerequisite requirements.
- **Course Scheduling**: Automatically generates a sequence of courses to be taken based on a four-year plan.
- **Credits Extraction**: Extracts the credit value from course descriptions.
- **Prerequisite Cleanup**: Cleans and processes prerequisite information from raw data.

## Files

- **`Degree_Scheduler.py`**:
  - Handles course management logic.
  - Key functions:
    - `is_in_arr()`: Checks if a course is in the list of taken courses.
    - `normalize_string()`: Strips whitespace and converts course names to uppercase for consistency.
    - `eliminate_previous()`: Filters out courses that have already been taken or courses that are lower-ranked in the curriculum.

- **`Courses_table.py`**:
  - Manages course data using the pandas library.
  - Key functions:
    - `extract_credits()`: Extracts credit information from course names using regular expressions.
    - `clean_prerequisites()`: Removes unnecessary text from prerequisite descriptions.
    - `split_course_code()`: Parses the course code into department and number for easier processing.

## How to Use

1. **Clone the Repository**: 
   ```bash
   git clone <repository-link>
   cd degree-scheduler
   ```

2. **Prepare Course Data**:
   Ensure you have a CSV file (`uo_courses_with_prerequisites.csv`) with the course information, including prerequisites and credits.

3. **Run the Scheduler**:
   You can start scheduling courses by running the `Degree_Scheduler.py` and start inputing courses you've already taken.
