document.getElementById("loginForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const res = await fetch("/api/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            email: document.getElementById("username").value,
            password: password.value
        })
    });

    const data = await res.json();

    if (res.ok) {
        localStorage.setItem("token", data.access_token);
        alert("Login successful!");
        window.location.href = "../pages/dashboard.html";
    } else {
        alert(data.error || "Login failed");
    }
});