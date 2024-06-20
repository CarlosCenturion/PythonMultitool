document.addEventListener('DOMContentLoaded', () => {
    const editUserForm = document.getElementById('editUserForm');
    const backButton = document.getElementById('backButton');

    const user = JSON.parse(localStorage.getItem('user'));
    if (!user || user.permissions !== 'admin') {
        window.location.href = '/login';
        return;
    }

    const urlParams = new URLSearchParams(window.location.search);
    const userId = urlParams.get('id');

    fetch(`/user/${userId}`)
        .then(response => response.json())
        .then(user => {
            document.getElementById('editUserName').value = user.name;
            document.getElementById('editUserEmail').value = user.email;
            document.getElementById('editUserPassword').value = '';
            document.getElementById('editUserPermissions').value = user.permissions;
        });

    editUserForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const name = document.getElementById('editUserName').value;
        const email = document.getElementById('editUserEmail').value;
        const password = document.getElementById('editUserPassword').value;
        const permissions = document.getElementById('editUserPermissions').value;

        const response = await fetch(`/user/${userId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, email, password, permissions })
        });

        const result = await response.json();
        if (response.ok) {
            alert('User updated successfully');
            window.location.href = '/view-users';
        } else {
            alert(result.error);
        }
    });

    backButton.addEventListener('click', () => {
        window.location.href = '/admin';
    });
});
