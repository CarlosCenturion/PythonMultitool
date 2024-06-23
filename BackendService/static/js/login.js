document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');

    loginForm.addEventListener('submit', async (event) => {

        console.log("AHHHH");
        event.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        try {
            const response = await fetch('/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name: username, password: password })
            });

            if (response.ok) {
                const user = await response.json();
                localStorage.setItem('user', JSON.stringify(user));
                window.location.href = '/';
            } else {
                const error = await response.json();
                document.getElementById('error').textContent = error.error;
            }
        } catch (error) {
            console.error('Error logging in:', error);
            document.getElementById('error').textContent = 'An error occurred';
        }
    });
});
