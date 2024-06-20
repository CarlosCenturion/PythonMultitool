document.addEventListener('DOMContentLoaded', () => {
    const settingsForm = document.getElementById('settingsForm');
    const backButton = document.getElementById('backButton');

    const user = JSON.parse(localStorage.getItem('user'));
    if (!user || user.permissions !== 'admin') {
        window.location.href = '/login';
        return;
    }

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
            alert('Settings updated successfully');
        } else {
            alert(result.error);
        }
    });

    backButton.addEventListener('click', () => {
        window.location.href = '/admin';
    });
});
