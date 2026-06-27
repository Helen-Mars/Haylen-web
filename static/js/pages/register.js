document.addEventListener('DOMContentLoaded', function() {

    const form = document.getElementById('registerForm');
    const username = document.getElementById('username');
    const email = document.getElementById('email');
    const password = document.getElementById('password');
    const confirmPassword = document.getElementById('confirmPassword');
    const toggleBtn = document.getElementById('togglePassword');
    const strengthBar = document.getElementById('strengthBar');
    const strengthText = document.getElementById('strengthText');
    const confirmHelp = document.getElementById('confirmHelp');
    const alertPlaceholder = document.getElementById('alertPlaceholder');
    const registerBtn = document.getElementById('registerBtn');
    const btnText = document.getElementById('btnText');
    const btnSpinner = document.getElementById('btnSpinner');

    // ── 密码显示/隐藏 ─────────────────────────────────────────────
    toggleBtn.addEventListener('click', function() {
        const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
        password.setAttribute('type', type);
        this.querySelector('i').className = type === 'password' ? 'bi bi-eye' : 'bi bi-eye-slash';
    });

    // ── 密码强度 ──────────────────────────────────────────────────
    password.addEventListener('input', function() {
        const val = this.value;
        const strength = getStrength(val);
        const colors = ['', 'bg-danger', 'bg-warning', 'bg-info', 'bg-success'];
        const labels = ['', 'Weak', 'Fair', 'Good', 'Strong'];

        strengthBar.className = 'strength-bar ' + colors[strength];
        strengthBar.style.width = (strength * 25) + '%';
        strengthText.textContent = strength ? labels[strength] : 'Enter a password';
        strengthText.className = 'form-text' + (strength ? ' text-' + ['', 'danger', 'warning', 'info', 'success'][strength] : '');
    });

    function getStrength(pw) {
        if (!pw) return 0;
        let score = 0;
        if (pw.length >= 6) score++;
        if (pw.length >= 10) score++;
        if (/[A-Z]/.test(pw) && /[a-z]/.test(pw)) score++;
        if (/\d/.test(pw)) score++;
        if (/[^A-Za-z0-9]/.test(pw)) score++;
        if (pw.length >= 14) score++;
        return Math.min(4, Math.floor(score / 1.5));
    }

    // ── 确认密码匹配 ──────────────────────────────────────────────
    confirmPassword.addEventListener('input', function() {
        if (this.value) {
            if (this.value === password.value) {
                confirmHelp.textContent = 'Passwords match';
                confirmHelp.className = 'form-text text-success';
            } else {
                confirmHelp.textContent = 'Passwords do not match';
                confirmHelp.className = 'form-text text-danger';
            }
        } else {
            confirmHelp.textContent = '';
            confirmHelp.className = 'form-text';
        }
    });

    password.addEventListener('input', function() {
        if (confirmPassword.value) {
            confirmPassword.dispatchEvent(new Event('input'));
        }
    });

    // ── 显示提示消息 ──────────────────────────────────────────────
    function showAlert(message, type) {
        alertPlaceholder.innerHTML =
            '<div class="alert alert-' + type + ' alert-dismissible fade show" role="alert">' +
            message +
            '<button type="button" class="btn-close" data-bs-dismiss="alert"></button>' +
            '</div>';
    }

    // ── 表单提交 ──────────────────────────────────────────────────
    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        // 前端校验
        if (password.value !== confirmPassword.value) {
            showAlert('Passwords do not match.', 'danger');
            return;
        }
        if (password.value.length < 6) {
            showAlert('Password must be at least 6 characters.', 'danger');
            return;
        }
        if (!email.value) {
            showAlert('Please enter your email.', 'danger');
            return;
        }
        if (!username.value) {
            showAlert('Please enter a username.', 'danger');
            return;
        }

        // 加载状态
        registerBtn.disabled = true;
        btnText.textContent = 'Registering...';
        btnSpinner.classList.remove('d-none');
        alertPlaceholder.innerHTML = '';

        try {
            const response = await fetch('/api/v1/authing/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    username: username.value.trim(),
                    email: email.value.trim(),
                    password: password.value
                })
            });

            if (response.ok) {
                showAlert('Registration successful! Redirecting...', 'success');
                form.reset();
                setTimeout(function() {
                    window.location.href = '/';
                }, 1500);
            } else {
                const data = await response.json();
                const detail = data.detail
                    ? (Array.isArray(data.detail)
                        ? data.detail.map(function(d) { return d.msg; }).join(', ')
                        : data.detail)
                    : 'Registration failed. Please try again.';
                showAlert(detail, 'danger');
            }
        } catch (error) {
            showAlert('Network error. Please check your connection.', 'danger');
        } finally {
            registerBtn.disabled = false;
            btnText.textContent = 'Register';
            btnSpinner.classList.add('d-none');
        }
    });

});