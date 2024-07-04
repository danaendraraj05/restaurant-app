// visited.js

document.addEventListener('DOMContentLoaded', function() {
    const visitedToggleBtn = document.getElementById('visited-toggle-btn');
    if (visitedToggleBtn) {
        visitedToggleBtn.addEventListener('click', function() {
            const restaurantId = this.getAttribute('data-restaurant-id');
            const url = `/restaurant/${restaurantId}/visited_toggle/`;

            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'), // Ensure you have a function to get CSRF token
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.action === 'add') {
                    visitedToggleBtn.textContent = 'Remove from Visited';
                } else if (data.action === 'remove') {
                    visitedToggleBtn.textContent = 'Mark as Visited';
                }
            })
            .catch(error => {
                console.error('Error toggling visited status:', error);
            });
        });
    }
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
