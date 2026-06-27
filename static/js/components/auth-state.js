const authArea = document.getElementById("auth-area");

function renderGuestState() {
    authArea.replaceChildren();

    const loginLink = document.createElement("a");
    loginLink.href = "/login";
    loginLink.className = "btn btn-outline-primary btn-sm";
    loginLink.textContent = "Login";

    const registerLink = document.createElement("a");
    registerLink.href = "/register";
    registerLink.className = "btn btn-outline-primary btn-sm";
    registerLink.textContent = "Register";

    authArea.append(loginLink, registerLink);
}

function renderUserState(user) {
    authArea.replaceChildren();

    const greeting = document.createElement("span");
    greeting.className = "text-body-secondary me-2";
    greeting.textContent = `Hi, ${user.username}`;

    const logoutBtn = document.createElement("button");
    logoutBtn.type = "button";
    logoutBtn.className = "btn btn-outline-secondary btn-sm";
    logoutBtn.textContent = "Logout";

    logoutBtn.addEventListener("click", async () => {
        try {
            await fetch("/api/v1/authing/logout", {
                method: "POST",
                credentials: "same-origin",
            });
        } catch {
            // ignore
        }
        window.location.href = "/";
    });

    authArea.append(greeting, logoutBtn);
}

async function loadAuthState() {
    if (!authArea) return;

    try {
        const response = await fetch("/api/v1/authing/users/me", {
            credentials: "same-origin",
        });

        if (!response.ok) {
            renderGuestState();
            return;
        }

        const data = await response.json();
        // API returns { "user": { "id": ..., "username": ..., "email": ... } }
        if (data.user) {
            renderUserState(data.user);
        } else {
            renderGuestState();
        }
    } catch {
        renderGuestState();
    }
}

loadAuthState();
