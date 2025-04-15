/**
 * TutorConnect Authentication Helper
 * This file handles user authentication state across pages.
 */

// Check login status when page loads
document.addEventListener("DOMContentLoaded", () => {
    updateUIBasedOnLoginState();
});

// Function to check if user is logged in
function isLoggedIn() {
    return localStorage.getItem('is_logged_in') === 'true';
}

// Function to get current user details
function getCurrentUser() {
    if (!isLoggedIn()) return null;
    
    return {
        id: localStorage.getItem('user_id'),
        name: localStorage.getItem('user_name'),
        email: localStorage.getItem('user_email'),
        role: localStorage.getItem('user_role')
    };
}

// Function to update UI based on login state
function updateUIBasedOnLoginState() {
    const isUserLoggedIn = isLoggedIn();
    const navLoginEl = document.querySelector('.nav-login');
    const navProfileEl = document.querySelector('.nav-profile');
    const navLogoutEl = document.querySelector('.nav-logout');
    const userGreetingEl = document.querySelector('.user-greeting');
    
    // Handle navigation items if they exist
    if (navLoginEl) {
        navLoginEl.style.display = isUserLoggedIn ? 'none' : 'block';
    }
    
    if (navProfileEl) {
        navProfileEl.style.display = isUserLoggedIn ? 'block' : 'none';
    }
    
    if (navLogoutEl) {
        navLogoutEl.style.display = isUserLoggedIn ? 'block' : 'none';
    }
    
    // Update user greeting if element exists
    if (userGreetingEl && isUserLoggedIn) {
        const user = getCurrentUser();
        userGreetingEl.textContent = `Welcome, ${user.name}!`;
        userGreetingEl.style.display = 'block';
    } else if (userGreetingEl) {
        userGreetingEl.style.display = 'none';
    }
    
    // Dispatch event so other scripts can respond to auth state
    document.dispatchEvent(new CustomEvent('authStateChanged', { 
        detail: { isLoggedIn: isUserLoggedIn, user: getCurrentUser() } 
    }));
}

// Function to log out user
function logout() {
    // Clear auth data from localStorage
    localStorage.removeItem('user_id');
    localStorage.removeItem('user_name');
    localStorage.removeItem('user_email');
    localStorage.removeItem('user_role');
    localStorage.removeItem('is_logged_in');
    
    // Update UI
    updateUIBasedOnLoginState();
    
    // Redirect to login page
    window.location.href = 'login.html';
}

// Export functions for other scripts
window.TutorConnectAuth = {
    isLoggedIn,
    getCurrentUser,
    updateUIBasedOnLoginState,
    logout
}; 