document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const betForm = document.getElementById('betForm');
    const settingsForm = document.getElementById('settingsForm');
    const logoutButton = document.getElementById('logoutButton');
    const updatePozoForm = document.getElementById('updatePozoForm');
    const adminSection = document.getElementById('adminSection');
    const settingsSection = document.getElementById('settingsSection');
    const createUserForm = document.getElementById('createUserForm');
    const viewUsersButton = document.getElementById('viewUsersButton');
    const usersList = document.getElementById('usersList');
    const resultMessage = document.getElementById('result');

    // Verificar si el usuario está logeado
    const user = JSON.parse(localStorage.getItem('user'));

    if (!user && window.location.pathname !== '/login') {
        // Si no hay usuario y no estamos en la página de login, redirigir a login
        window.location.href = '/login';
    }

    if (loginForm) {
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
    }

    if (betForm) {
        if (user) {
            document.getElementById('username').textContent = user.name;
            document.getElementById('balance').textContent = user.saldo;

            // Fetch the current pozo amount
            fetch('/pozo')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('pozo').textContent = data.pozo;
                });

            betForm.addEventListener('submit', async (event) => {
                event.preventDefault();
                const amount = document.getElementById('amount').value;

                const response = await fetch(`/user/${user.id}/apostar`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ cantidad: amount })
                });

                const result = await response.json();
                if (response.ok) {
                    user.saldo = result.nuevo_saldo;
                    localStorage.setItem('user', JSON.stringify(user));
                    document.getElementById('balance').textContent = user.saldo;
                    document.getElementById('pozo').textContent = result.nuevo_pozo;

                    resultMessage.textContent = `You ${result.resultado} and your new balance is ${result.nuevo_saldo}`;
                    if (result.resultado === "ganaste") {
                        resultMessage.classList.add('success');
                    } else {
                        resultMessage.classList.remove('success');
                    }
                } else {
                    resultMessage.textContent = result.error;
                }
            });
        } else {
            // Redirigir a login si el usuario no está logeado
            window.location.href = '/login';
        }
    }

    if (settingsForm) {
        if (user && user.permissions === 'admin') {
            settingsSection.style.display = 'block';

            fetch('/settings')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('winProbability').value = data.win_probability;
                    document.getElementById('maxWins').value = data.max_wins;
                });

            settingsForm.addEventListener('submit', async (event) => {
                event.preventDefault();
                const winProbability = document.getElementById('winProbability').value;
                const maxWins = document.getElementById('maxWins').value;

                const response = await fetch('/settings', {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ win_probability: winProbability, max_wins: maxWins })
                });

                const result = await response.json();
                if (response.ok) {
                    document.getElementById('result').textContent = 'Settings updated successfully';
                } else {
                    document.getElementById('result').textContent = result.error;
                }
            });
        }
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

    if (user && user.permissions === 'admin') {
        adminSection.style.display = 'block';

        updatePozoForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const amount = document.getElementById('pozoAmount').value;

            const response = await fetch('/pozo', {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ amount: amount })
            });

            const result = await response.json();
            if (response.ok) {
                document.getElementById('pozo').textContent = amount;
                document.getElementById('result').textContent = 'Pozo updated successfully';
            } else {
                document.getElementById('result').textContent = result.error;
            }
        });

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
                document.getElementById('result').textContent = 'User created successfully';
            } else {
                document.getElementById('result').textContent = result.error;
            }
        });

        viewUsersButton.addEventListener('click', async () => {
            const response = await fetch('/users', {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' }
            });

            const users = await response.json();
            if (response.ok) {
                usersList.innerHTML = '';  // Clear previous list
                users.forEach(user => {
                    const userElement = document.createElement('div');
                    userElement.textContent = `ID: ${user[0]}, Name: ${user[1]}, Email: ${user[2]}, Permissions: ${user[3]}, Balance: ${user[4]}`;
                    usersList.appendChild(userElement);
                });
                usersList.style.display = 'block';
            } else {
                document.getElementById('result').textContent = 'Error fetching users';
            }
        });
    }
});
