document.addEventListener('DOMContentLoaded', () => {
    const betForm = document.getElementById('betForm');
    const logoutButton = document.getElementById('logoutButton');
    const resultMessage = document.getElementById('result');
    const settingsSection = document.getElementById('settingsSection');
    const adminSection = document.getElementById('adminSection');

    const user = JSON.parse(localStorage.getItem('user'));
    if (!user) {
        window.location.href = '/login';
        return;
    }

    document.getElementById('username').textContent = user.name;
    document.getElementById('balance').textContent = user.saldo;

    fetch('/pozo')
        .then(response => response.json())
        .then(data => {
            document.getElementById('pozo').textContent = data.pozo;
        });

    if (user.permissions === 'admin') {
        settingsSection.classList.remove('hidden');
        adminSection.classList.remove('hidden');

        fetch('/settings')
            .then(response => response.json())
            .then(data => {
                document.getElementById('winProbability').value = data.win_probability;
                document.getElementById('maxWins').value = data.max_wins;
            });

        document.getElementById('settingsForm').addEventListener('submit', async (event) => {
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
                document.getElementById('result').classList.add('success');
            } else {
                document.getElementById('result').textContent = result.error;
                document.getElementById('result').classList.remove('success');
            }
        });
    }

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
