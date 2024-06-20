document.addEventListener('DOMContentLoaded', () => {
    const createUserForm = document.getElementById('createUserForm');
    const backButton = document.getElementById('backButton');

    const user = JSON.parse(localStorage.getItem('user'));
    if (!user || user.permissions !== 'admin') {
        window.location.href = '/login';
        return;
    }

    createUserForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const name = document.getElementById('newUserName').value;
        const email = document.getElementById('newUserEmail').value;
        const password = document.getElementById('newUserPassword').value;
        const permissions = document.getElementById('newUserPermissions').value;

        const response = await fetch('/user', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, email, password, permissions })
        });

        const result = await response.json();
        if (response.ok) {
            alert('User created successfully');
            createUserForm.reset();
        } else {
            alert(result.error);
        }
    });

    backButton.addEventListener('click', () => {
        window.location.href = '/admin';
    });
});
