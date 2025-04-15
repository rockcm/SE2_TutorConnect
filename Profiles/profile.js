/**
 * TutorConnect Profile Page
 * Loads and displays user data from localStorage
 */

document.addEventListener("DOMContentLoaded", function() {
    // Get user data from local storage
    const userData = TutorConnectAuth.getCurrentUser();
    
    if (!userData) {
        console.error('No user data found');
        return;
    }
    
    // Populate profile data
    populateUserProfile(userData);
    
    // Show appropriate section based on user role
    showRoleSpecificSection(userData.role);
    
    // Set up event listeners
    document.querySelector('.edit-btn').addEventListener('click', function() {
        alert("Edit profile functionality will be implemented soon!");
    });
    
    document.querySelector('.save-btn').addEventListener('click', function() {
        alert("Changes saved successfully!");
    });
});

/**
 * Populates the user profile with data from localStorage
 */
function populateUserProfile(userData) {
    // Update basic profile information
    document.getElementById('user-name').textContent = userData.name || 'User';
    document.getElementById('user-email').textContent = userData.email || 'No email provided';
    document.getElementById('user-role').textContent = userData.role || 'User';
    
    // Set username in profile
    const usernameEl = document.querySelector('.profile-header p');
    if (usernameEl && userData.email) {
        // Create a username from email
        const username = userData.email.split('@')[0];
        usernameEl.textContent = `@${username}`;
    }
    
    // Update page title
    document.title = `${userData.name}'s Profile - TutorConnect`;
}

/**
 * Shows or hides sections based on user role
 */
function showRoleSpecificSection(role) {
    const studentSection = document.getElementById('student-section');
    const tutorSection = document.getElementById('tutor-section');
    
    // Default to hiding both
    studentSection.style.display = 'none';
    tutorSection.style.display = 'none';
    
    // Show appropriate section based on role
    if (role && role.toLowerCase() === 'student') {
        studentSection.style.display = 'block';
    } else if (role && role.toLowerCase() === 'tutor') {
        tutorSection.style.display = 'block';
    } else {
        // If role is undefined or something else, show a message
        console.log('Unknown role:', role);
    }
}