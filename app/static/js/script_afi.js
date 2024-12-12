function toggleDetails(card) {
    // Hilangkan status 'clicked' dari semua kartu lainnya
    document.querySelectorAll('.affiliate-item').forEach(item => {
        if (item !== card) {
            item.classList.remove('clicked');
        }
    });

    // Toggle status 'clicked' pada kartu yang diklik
    card.classList.toggle('clicked');
}

document.addEventListener('DOMContentLoaded', function () {
    const hamburgerMenu = document.getElementById('hamburger-menu');
    const dropdownMenu = document.getElementById('dropdown-menu');

    // Toggle menu
    hamburgerMenu.addEventListener('click', function () {
        dropdownMenu.classList.toggle('show');
        hamburgerMenu.classList.toggle('open');
    });
});