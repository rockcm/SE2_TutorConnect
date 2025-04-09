document.addEventListener("DOMContentLoaded", () => {
  const loginForm = document.getElementById("loginForm");
  const signupForm = document.getElementById("signupForm");
  const formTitle = document.getElementById("formTitle");
  const showLoginBtn = document.getElementById("showLogin");
  const showSignupBtn = document.getElementById("showSignup");

  // Toggle Forms
  showLoginBtn.addEventListener("click", () => {
      loginForm.classList.remove("hidden");
      signupForm.classList.add("hidden");
      formTitle.textContent = "Login";
      showLoginBtn.classList.add("active");
      showSignupBtn.classList.remove("active");
  });

  showSignupBtn.addEventListener("click", () => {
      signupForm.classList.remove("hidden");
      loginForm.classList.add("hidden");
      formTitle.textContent = "Sign Up";
      showSignupBtn.classList.add("active");
      showLoginBtn.classList.remove("active");
  });

  // Login Form Submission
  loginForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      const email = document.getElementById("loginEmail").value;
      const password = document.getElementById("loginPassword").value;

      const response = await fetch("http://localhost:8000/login", {
          method: "POST",
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
          body: new URLSearchParams({ username: email, password })
      });

      const data = await response.json();
      if (response.ok) {
          localStorage.setItem("token", data.access_token);
          alert("Login successful!");
          window.location.href = "dashboard.html";
      } else {
          alert(data.detail);
      }
  });

  // Signup Form Submission
  signupForm.addEventListener("submit", (event) => {
      // With HTMX handling the form submission to create a user,
      // we don't need to prevent default or use fetch anymore.
      // Just let HTMX do its job.
      
      // We could add any additional client-side validation here if needed
      const name = document.getElementById("signupName").value;
      const email = document.getElementById("signupEmail").value;
      const password = document.getElementById("signupPassword").value;
      
      // Log the submission (for debugging)
      console.log("Submitting signup form via HTMX");
  });

  // Listen for successful registration via HTMX
  document.body.addEventListener("htmx:afterSwap", function(event) {
      // Check if the swap target was our signup-result area
      if (event.detail.target.id === "signup-result") {
          // If the response contains a table element, it was successful
          if (event.detail.target.querySelector("table")) {
              setTimeout(() => {
                  alert("Registration successful! Please log in.");
                  // Switch to login form
                  showLoginBtn.click();
              }, 500);
          }
      }
  });
});
