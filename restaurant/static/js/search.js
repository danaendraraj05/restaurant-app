document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    const restaurantCards = document.querySelectorAll('.restaurant-card');

    searchInput.addEventListener('input', function() {
        const searchTerm = searchInput.value.trim().toLowerCase();

        restaurantCards.forEach(card => {
            const titleElement = card.querySelector('.restaurant-title');
            const title = titleElement.textContent.trim().toLowerCase();

            if (title.includes(searchTerm)) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    });
});