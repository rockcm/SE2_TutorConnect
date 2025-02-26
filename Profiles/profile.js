document.addEventListener("DOMContentLoaded", function() {
    // Change this variable to "Student", "Tutor", or "Both"
    let userRole = "Student"; // Toggle between "Student", "Tutor", or "Both"

    // Get the sections
    let studentSection = document.getElementById("student-section");
    let tutorSection = document.getElementById("tutor-section");
    let roleDisplay = document.getElementById("user-role");

    // Set displayed role in profile card
    roleDisplay.textContent = userRole;

    // Toggle visibility based on role
    if (userRole === "Student") {
        tutorSection.style.display = "none"; // Hide tutor section
        studentSection.style.display = "block"; // Show student section
    } else if (userRole === "Tutor") {
        studentSection.style.display = "none"; // Hide student section
        tutorSection.style.display = "block"; // Show tutor section
    } else {
        // Show both sections if role is "Both"
        studentSection.style.display = "block";
        tutorSection.style.display = "block";
    }
});