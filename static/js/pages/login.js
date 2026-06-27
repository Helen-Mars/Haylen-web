document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("loginForm");
  const username = document.getElementById("username");
  const password = document.getElementById("password");
  const toggleBtn = document.getElementById("togglePassword");
  const alertPlaceholder = document.getElementById("alertPlaceholder");
  const loginBtn = document.getElementById("loginBtn");
  const btnText = document.getElementById("btnText");
  const btnSpinner = document.getElementById("btnSpinner");
  const rememberMe = document.getElementById("rememberMe");

  // ── 密码显示/隐藏 ─────────────────────────────────────────────
  toggleBtn.addEventListener("click", function () {
    const type =
      password.getAttribute("type") === "password" ? "text" : "password";
    password.setAttribute("type", type);
    this.querySelector("i").className =
      type === "password" ? "bi bi-eye" : "bi bi-eye-slash";
  });

  // ── 显示提示消息 ──────────────────────────────────────────────
  function showAlert(message, type) {
    alertPlaceholder.innerHTML =
      '<div class="alert alert-' +
      type +
      ' alert-dismissible fade show" role="alert">' +
      message +
      '<button type="button" class="btn-close" data-bs-dismiss="alert"></button>' +
      "</div>";
  }

  // ── 表单提交 ──────────────────────────────────────────────────
  form.addEventListener("submit", async function (e) {
    e.preventDefault();

    if (!username.value.trim()) {
      showAlert("Please enter your username.", "danger");
      return;
    }
    if (!password.value) {
      showAlert("Please enter your password.", "danger");
      return;
    }

    // 加载状态
    loginBtn.disabled = true;
    btnText.textContent = "Signing in...";
    btnSpinner.classList.remove("d-none");
    alertPlaceholder.innerHTML = "";

    try {
      const response = await fetch("/api/v1/authing/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          username: username.value.trim(),
          password: password.value,
          remember_me: rememberMe.checked,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        // httpOnly cookie 已由后端根据 remember_me 设置过期时间
        showAlert("Login successful! Redirecting...", "success");
        setTimeout(function () {
          window.location.href = "/";
        }, 1000);
      } else {
        const detail =
          data.detail || "Login failed. Please check your credentials.";
        showAlert(detail, "danger");
      }
    } catch (error) {
      showAlert("Network error. Please check your connection.", "danger");
    } finally {
      loginBtn.disabled = false;
      btnText.textContent = "Sign In";
      btnSpinner.classList.add("d-none");
    }
  });

  // ── Enter 键快速提交 ──────────────────────────────────────────
  password.addEventListener("keydown", function (e) {
    if (e.key === "Enter") {
      form.dispatchEvent(new Event("submit"));
    }
  });
});
