function isInArr(input, ourArr) {
    for (let elem of ourArr) {
        if (elem === input) {
            return true;
        }
    }
    return false;
}

function normalizeString(input) {
    return input.trim().toUpperCase();
}

function eliminatePrevious(courses, coursesTaken) {
    const takenCoursesList = coursesTaken.split(',').map(course => normalizeString(course));

    let maxIndex = -1;
    for (let takenCourse of takenCoursesList) {
        if (courses.includes(takenCourse)) {
            maxIndex = Math.max(maxIndex, courses.indexOf(takenCourse));
        }
    }

    return maxIndex !== -1 ? courses.slice(maxIndex + 1) : courses;
}

function buildTermSchedule(csClasses, mtClasses, sciClasses, currentYear) {
    const fall = ["CS102", "CS122", "CS210", "CS212", "CS313", "CS314", "CS322", "CS415", "CS425", "CS422", "CS431", "CS432", "CS443", "CS451", "CS471", "CS410", "DSCI311", "CS455", "CS413", "J431"];
    const winter = ["CS102", "CS122", "CS210", "CS211", "CS313", "CS314", "CS315", "CS330", "CS333", "CS372M", "CS422", "CS429", "CS433", "CS445", "CS453", "CS410", "CS455", "CS413", "J431"];
    const spring = ["CS102", "CS122", "CS210", "CS211", "CS212", "CS315", "CS322", "CS330", "CS415", "CS425", "CS422", "CS423", "CS434", "CS436", "CS472", "CS473", "CS410", "CS455", "CS413", "J431"];
    const terms = { "Fall": fall, "Winter": winter, "Spring": spring };

    let remainingCSClasses = [...csClasses];
    let remainingMTClasses = [...mtClasses];
    let remainingSCIClasses = [...sciClasses];
    let remainingWRClasses = ["WR121", "WR123", "WR320"];
    let remainingGenEd = ["A&L", "A&L", "A&L", "A&L", "SSC", "SSC", "SSC", "SSC", "GP", "US"];

    let year = currentYear;

    let scheduleHtml = ''; // To store the final HTML to display

    while (remainingCSClasses.length > 0 || remainingMTClasses.length > 0 || remainingSCIClasses.length > 0 || remainingWRClasses.length > 0 || remainingGenEd.length > 0) {
        scheduleHtml += `<h3>Year ${year} Schedule:</h3><ul>`;
        let termSchedule = {
            "Fall": [],
            "Winter": [],
            "Spring": []
        };

        for (let term in termSchedule) {
            let cs313Taken = !remainingCSClasses.includes("CS313"); 
            let maxCSPerTerm = cs313Taken ? 2 : 1;

            let csCount = 0;
            let iterCS = 0;
            while (csCount < maxCSPerTerm && iterCS < remainingCSClasses.length) {
                let selectedCS = remainingCSClasses[iterCS];

                if (terms[term].includes(selectedCS)) {
                    termSchedule[term].push(selectedCS);
                    remainingCSClasses.splice(iterCS, 1);
                    csCount++;
                } else {
                    iterCS++;
                }
            }

            if (remainingMTClasses.length > 0) {
                termSchedule[term].push(remainingMTClasses.shift());
            }

            if (remainingSCIClasses.length > 0) {
                termSchedule[term].push(remainingSCIClasses.shift());
            }

            while (termSchedule[term].length < 4) {
                if (remainingWRClasses.length > 0 && year > 2) {
                    termSchedule[term].push(remainingWRClasses.shift());
                } else if (remainingWRClasses.length > 0 && remainingWRClasses[0] !== "WR320") {
                    termSchedule[term].push(remainingWRClasses.shift());
                }

                if (remainingGenEd.length > 0) {
                    let randomGenEdCourse = remainingGenEd.splice(Math.floor(Math.random() * remainingGenEd.length), 1)[0];
                    termSchedule[term].push(randomGenEdCourse);
                }
                break;
            }
        }

        for (let term in termSchedule) {
            if (termSchedule[term].length > 0) {
                scheduleHtml += `<li><strong>${term}</strong>: ${termSchedule[term].join(', ')}</li>`;
            }
        }
        scheduleHtml += '</ul>';

        year += 1;
        if (year >= 10) {
            break;
        }
    }

    document.getElementById("schedule-output").innerHTML = scheduleHtml;
}

function getYear(year) {
    const collegeYear = {
        "FRESHMAN": 1,
        "SOPHOMORE": 2,
        "JUNIOR": 3,
        "SENIOR": 4
    };

    const normalizedYear = normalizeString(year);
    return collegeYear[normalizedYear] || 0;
}

function csScienceReq() {
    // Define your science requirements (dummy data here)
    const csPhysics = [['PHYS201', 'PHYS202', 'PHYS203'], ['PHYS251', 'PHYS252', 'PHYS253']];
    const csChemistry = [['CH221', 'CH222', 'CH223'], ['CH224H', 'CH225H', 'CH226H']];
    const csGeography = ['GEOG141', ['GEOG 321', 'GEOG322', 'GEOG323']];
    const csGeology = ['ERTH201', 'ERTH202', 'ERTH203'];
    const csPsychology = ['PSY201', ['PSY301', 'PSY304', 'PSY305', 'PSY348']];
    const csBiology = [["BI211", "BI212", "BI213"], ["CH111", "CH113", "CH221", "CH224H"], ["BI212", "BI213"]];

    return csPhysics; // For demonstration, you can allow users to select from these sequences.
}

function main() {
    const csClasses = ["CS122", "CS210", "CS211", "CS212", "CS313", "CS314", "CS315", "CS330", "CS415", "CS422", "CS425"];
    const mtClasses = ["MATH231", "MATH232", "MATH251", "MATH252", "MATH253", "MATH341", "MATH342"];

    const selectedMajor = document.getElementById("major").value; // Get the selected major from the form
    const year = document.getElementById("year").value; // Get the year from the form

    const currentYear = getYear(year);
    if (currentYear === 0) {
        alert("Invalid year. Please enter Freshman, Sophomore, Junior, or Senior.");
        return;
    }

    const selectedSCIClasses = csScienceReq(); // You can customize this to select the science requirement
    let remainingSCIClasses = eliminatePrevious(selectedSCIClasses, ""); // Adjust based on taken courses
    let remainingCSClasses = eliminatePrevious(csClasses, ""); // Adjust based on taken courses
    let remainingMTClasses = eliminatePrevious(mtClasses, ""); // Adjust based on taken courses

    buildTermSchedule(remainingCSClasses, remainingMTClasses, remainingSCIClasses, currentYear);
}

document.getElementById("submit-button").addEventListener("click", main);
