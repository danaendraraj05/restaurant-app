
    // JavaScript to toggle the filter overlay
    document.addEventListener('DOMContentLoaded', function() {
        const filterBtn = document.getElementById('filter-btn');
        const filterOverlay = document.getElementById('filter-overlay');
        const closeFilterBtn = document.getElementById('close-filter-btn');
        

        filterBtn.addEventListener('click', function() {
            filterOverlay.style.display = 'flex'; 
        });

        closeFilterBtn.addEventListener('click', function() {
            filterOverlay.style.display = 'none'; 
        });
    });
