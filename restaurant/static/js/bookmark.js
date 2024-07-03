// bookmark.js

document.addEventListener('DOMContentLoaded', function() {
    const bookmarkToggleBtn = document.getElementById('bookmark-toggle-btn');
    if (bookmarkToggleBtn) {
        bookmarkToggleBtn.addEventListener('click', function() {
            const restaurantId = this.getAttribute('data-restaurant-id');
            const url = `/restaurant/${restaurantId}/bookmark/`;

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
                    bookmarkToggleBtn.textContent = 'Remove Bookmark';
                } else if (data.action === 'remove') {
                    bookmarkToggleBtn.textContent = 'Add Bookmark';
                }
            })
            .catch(error => {
                console.error('Error toggling bookmark:', error);
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
