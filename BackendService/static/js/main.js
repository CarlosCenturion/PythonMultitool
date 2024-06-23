document.addEventListener('DOMContentLoaded', () => {
    const betForm = document.getElementById('betForm');
    const logoutButton = document.getElementById('logoutButton');
    const resultMessage = document.getElementById('result');
    const settingsSection = document.getElementById('settingsSection');
    const adminSection = document.getElementById('adminSection');

    const user = JSON.parse(localStorage.getItem('user'));
    if (!user) {
        console.log("Se acaba de logear " + user);
        window.location.href = '/login';
        return;
    }

    document.getElementById('username').textContent = user.name;
    document.getElementById('balance').textContent = user.saldo;

    fetch('/pozo')
        .then(response => response.json())
        .then(data => {
            document.getElementById('pozo').textContent = data.pozo;
        })
        .catch(error => {
            console.error('Error fetching pozo:', error);
            window.location.href = '/login';
        });

    if (user.permissions === 'admin') {
        settingsSection.classList.remove('hidden');
        adminSection.classList.remove('hidden');
        console.error('Hay Admin:', error);
        fetch('/settings')
            .then(response => response.json())
            .then(data => {
                document.getElementById('winProbability').value = data.win_probability;
                document.getElementById('maxWins').value = data.max_wins;
            })
            .catch(error => {
                console.error('Error fetching settings:', error);
                window.location.href = '/login';
            });

        document.getElementById('settingsForm').addEventListener('submit', async (event) => {
            event.preventDefault();
            const winProbability = document.getElementById('winProbability').value;
            const maxWins = document.getElementById('maxWins').value;

            try {
                const response = await fetch('/settings', {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ win_probability: winProbability, max_wins: maxWins })
                });

                if (response.ok) {
                    const result = await response.json();
                    resultMessage.textContent = 'Settings updated successfully';
                    resultMessage.classList.add('success');
                } else {
                    const error = await response.json();
                    resultMessage.textContent = error.error;
                    resultMessage.classList.remove('success');
                }
            } catch (error) {
                console.error('Error updating settings:', error);
                resultMessage.textContent = 'An error occurred';
                resultMessage.classList.remove('success');
            }
        });
    }

    betForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const amount = document.getElementById('amount').value;

        try {
            const response = await fetch(`/user/${user.id}/apostar`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ cantidad: amount })
            });

            if (response.ok) {
                const result = await response.json();
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
                const error = await response.json();
                resultMessage.textContent = error.error;
            }
        } catch (error) {
            console.error('Error betting:', error);
            resultMessage.textContent = 'An error occurred';
        }
    });

    if (logoutButton) {
        logoutButton.addEventListener('click', async () => {
            try {
                const response = await fetch('/logout', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' }
                });

                if (response.ok) {
                    localStorage.removeItem('user');
                    window.location.href = '/login';
                }
            } catch (error) {
                console.error('Error logging out:', error);
            }
        });
    }
});
