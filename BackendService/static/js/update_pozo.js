document.addEventListener('DOMContentLoaded', () => {
    const updatePozoForm = document.getElementById('updatePozoForm');
    const backButton = document.getElementById('backButton');

    const user = JSON.parse(localStorage.getItem('user'));
    if (!user || user.permissions !== 'admin') {
        window.location.href = '/login';
        return;
    }

    updatePozoForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const amount = document.getElementById('pozoAmount').value;

        const response = await fetch('/pozo', {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ amount })
        });

        const result = await response.json();
        if (response.ok) {
            alert('Pozo updated successfully');
        } else {
            alert(result.error);
        }
    });

    backButton.addEventListener('click', () => {
        window.location.href = '/admin';
    });
});
