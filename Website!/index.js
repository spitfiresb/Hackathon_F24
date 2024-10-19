function getSelectedMajor() {
    const dropdown = document.getElementById("majors"); 
    const selectedMajor = dropdown.ariaValueMax; 
    console.log(selectedMajor); 
    return selectedMajor; 
}
