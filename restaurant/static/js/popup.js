document.addEventListener('DOMContentLoaded', function() {
    const filterBtn = document.getElementById('filter-btn');
    const filterOverlay = document.getElementById('filter-overlay');
    const closeFilterBtn = document.getElementById('close-filter-btn');

    filterBtn.addEventListener('click', function() {
        filterOverlay.style.display = 'flex'; // Show the overlay
    });

    closeFilterBtn.addEventListener('click', function() {
        filterOverlay.style.display = 'none'; // Hide the overlay
    });
});
