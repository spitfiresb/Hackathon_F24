function getSelectedMajor() {
    const dropdown = document.getElementById("majors"); 
    const selectedMajor = dropdown.value; 
    console.log(selectedMajor); 

    if (!selectedMajor) {
        alert("Please select a major before submitting."); 
        return; 
    }

    fetch("/courses/submit/", {  // Adjust the URL to match your Django routing
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ major: selectedMajor }),  // Send the selected major as JSON
    })
    .then(response => response.json())
    .then(data => {
        console.log(data); // Handle the response from the server
        if (data.status === "success") {
            // Process the courses received (data.courses)
            alert(`Courses to take: ${data.courses.join(", ")}`);
        } else {
            alert(data.message); // Show error message
        }
    })
    .catch(error => console.error("Error:", error)); // Handle any errors
}


