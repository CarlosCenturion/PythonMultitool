document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const betForm = document.getElementById('betForm');
    const settingsForm = document.getElementById('settingsForm');

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
                    document.getElementById('result').textContent = `You ${result.resultado} and your new balance is ${result.nuevo_saldo}`;
                } else {
                    document.getElementById('result').textContent = result.error;
                }
            });
        } else {
            // Redirigir a login si el usuario no está logeado
            window.location.href = '/login';
        }
    }

    if (settingsForm) {
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
});
