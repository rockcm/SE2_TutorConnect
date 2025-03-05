// This script listens for changes in the search bar and dropdown menus and based on the user input, will filter the list of tutors 
//The results are updated in real time.


document.addEventListener("DOMContentLoaded", function () {
    //references to elements in html
    const searchBar = document.getElementById("searchBar");
    const subjectFilter = document.getElementById("subject");
    const tutorList = document.getElementById("tutorList");
    const tutors = Array.from(tutorList.getElementsByClassName("tutor"));
  
    function filterTutors() {
        //makes everything the case case for pattern matching
      const searchQuery = searchBar.value.toLowerCase();
      const selectedSubject = subjectFilter.value.toLowerCase();

        //loops through each tutor, retrieves text, converts to lower, checks if the text contains the user's input, 
        // and checks if it matches subject selected OR all subjects
      tutors.forEach((tutor) => {
        const tutorText = tutor.textContent.toLowerCase();
        const isNameMatch = tutorText.includes(searchQuery);
        const isSubjectMatch = selectedSubject === "" || tutorText.includes(selectedSubject);

        //if it matches on tutor name AND subject selection, it will remain visible and the others are hidden
        if (isNameMatch && isSubjectMatch) {
          tutor.style.display = "list-item";
        } else {
          tutor.style.display = "none";
        }
      });
    }
  
    //listeners for change 
    searchBar.addEventListener("input", filterTutors);
    subjectFilter.addEventListener("change", filterTutors);
  });
  