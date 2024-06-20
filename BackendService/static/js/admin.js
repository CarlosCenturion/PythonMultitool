document.addEventListener('DOMContentLoaded', () => {
    const logoutButton = document.getElementById('logoutButton');

    const user = JSON.parse(localStorage.getItem('user'));
    if (!user || user.permissions !== 'admin') {
        window.location.href = '/login';
        return;
    }

    if (logoutButton) {
        logoutButton.addEventListener('click', async () => {
            const response = await fetch('/logout', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });

            if (response.ok) {
                localStorage.removeItem('user');
                window.location.href = '/login';
            }
        });
    }
});
