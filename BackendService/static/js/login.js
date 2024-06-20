document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');

    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        const response = await fetch('/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: username, password: password })
        });

        const result = await response.json();
        if (response.ok) {
            localStorage.setItem('user', JSON.stringify(result));
            window.location.href = '/';
        } else {
            document.getElementById('error').textContent = result.error;
        }
    });
});
