/*
 * js/auth.js
 * --------------------------------------------------------
 * Module owner : 2203137
 * Feature branch: feature/frontend-module
 * --------------------------------------------------------
 * Handles the login and registration forms and talks to the
 * auth API built by 2203136 (/api/auth/login, /api/auth/register).
 */

function showAlert(message, type = "danger") {
    const box = document.getElementById("alertBox");
    if (!box) return;
    box.textContent = message;
    box.className = "alert alert-" + type;
    box.style.display = "block";
}

document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("loginForm");
    if (loginForm) {
        loginForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const username = document.getElementById("username").value.trim();
            const password = document.getElementById("password").value;
            try {
                await api.post("/api/auth/login", { username, password });
                window.location.href = "dashboard.html";
            } catch (err) {
                showAlert(err.message);
            }
        });
    }

    const registerForm = document.getElementById("registerForm");
    if (registerForm) {
        registerForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const username = document.getElementById("username").value.trim();
            const password = document.getElementById("password").value;
            try {
                await api.post("/api/auth/register", { username, password });
                showAlert("Account created. Redirecting to login...", "success");
                setTimeout(() => (window.location.href = "index.html"), 1200);
            } catch (err) {
                showAlert(err.message);
            }
        });
    }
});
