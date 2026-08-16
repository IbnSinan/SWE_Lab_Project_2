/*
 * js/nav.js
 * --------------------------------------------------------
 * Module owner : 2203137
 * Feature branch: feature/frontend-module
 * --------------------------------------------------------
 * Shared by every authenticated page (dashboard, residents,
 * bills): checks that a session exists before showing the
 * page, fills in the logged-in username, and wires the
 * logout link. Pages that don't need this (login/register)
 * don't include this script.
 */

async function guardPage() {
    try {
        const result = await api.get("/api/auth/session");
        if (!result.logged_in) {
            window.location.href = "index.html";
            return;
        }
        const navUser = document.getElementById("navUser");
        if (navUser) navUser.textContent = "Hi, " + result.username;
    } catch (err) {
        window.location.href = "index.html";
    }
}

document.addEventListener("DOMContentLoaded", () => {
    guardPage();

    const logoutLink = document.getElementById("logoutLink");
    if (logoutLink) {
        logoutLink.addEventListener("click", async (e) => {
            e.preventDefault();
            await api.post("/api/auth/logout");
            window.location.href = "index.html";
        });
    }
});
