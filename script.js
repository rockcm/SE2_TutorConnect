document.getElementById("loginForm").addEventListener("submit", async function(event) {
    event.preventDefault(); // Prevent default form submission
    
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();
    
    if (!email || !password) {
        alert("Please enter both email and password.");
        return;
    }

    const payload = { email, password };
    
    try {
        const response = await fetch("http://127.0.0.1:8000/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            alert("User registered successfully!");
        } else {
            alert("Error: " + data.detail);
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Failed to connect to the server.");
    }
});
