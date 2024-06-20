document.addEventListener('DOMContentLoaded', () => {
    const backButton = document.getElementById('backButton');
    const usersTableBody = document.getElementById('usersTable').querySelector('tbody');
    const editBalanceModal = document.getElementById('editBalanceModal');
    const closeModalButton = document.getElementById('closeModalButton');
    const editBalanceForm = document.getElementById('editBalanceForm');
    let currentUserId = null;

    const user = JSON.parse(localStorage.getItem('user'));
    if (!user || user.permissions !== 'admin') {
        window.location.href = '/login';
        return;
    }

    fetch('/users')
        .then(response => response.json())
        .then(users => {
            users.forEach(user => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${user[0]}</td>
                    <td>${user[1]}</td>
                    <td>${user[2]}</td>
                    <td>${user[3]}</td>
                    <td>${user[4]}</td>
                    <td>
                        <button class="edit-user" data-id="${user[0]}">Edit</button>
                        <button class="delete-user" data-id="${user[0]}">Delete</button>
                        <button class="edit-balance" data-id="${user[0]}">Edit Balance</button>
                    </td>
                `;
                usersTableBody.appendChild(row);
            });

            document.querySelectorAll('.edit-user').forEach(button => {
                button.addEventListener('click', event => {
                    const userId = event.target.getAttribute('data-id');
                    window.location.href = `/edit-user?id=${userId}`;
                });
            });

            document.querySelectorAll('.delete-user').forEach(button => {
                button.addEventListener('click', async event => {
                    const userId = event.target.getAttribute('data-id');
                    const response = await fetch(`/user/${userId}`, {
                        method: 'DELETE',
                        headers: { 'Content-Type': 'application/json' }
                    });

                    const result = await response.json();
                    if (response.ok) {
                        event.target.parentElement.parentElement.remove();
                    } else {
                        alert(result.error);
                    }
                });
            });

            document.querySelectorAll('.edit-balance').forEach(button => {
                button.addEventListener('click', event => {
                    currentUserId = event.target.getAttribute('data-id');
                    editBalanceModal.classList.remove('hidden');
                });
            });
        });

    backButton.addEventListener('click', () => {
        window.location.href = '/admin';
    });

    closeModalButton.addEventListener('click', () => {
        editBalanceModal.classList.add('hidden');
    });

    editBalanceForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const newBalance = document.getElementById('editBalanceAmount').value;

        const response = await fetch(`/user/${currentUserId}/saldo`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ saldo: newBalance })
        });

        const result = await response.json();
        if (response.ok) {
            alert('Balance updated successfully');
            editBalanceModal.classList.add('hidden');
            window.location.reload();
        } else {
            alert(result.error);
        }
    });
});
