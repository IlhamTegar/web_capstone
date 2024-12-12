document.addEventListener('DOMContentLoaded', function () {
    const hamburgerMenu = document.getElementById('hamburger-menu');
    const dropdownMenu = document.getElementById('dropdown-menu');

    // Toggle menu
    hamburgerMenu.addEventListener('click', function () {
        dropdownMenu.classList.toggle('show');
        hamburgerMenu.classList.toggle('open');
    });

    const cards = document.querySelectorAll('.feature-card'); // Pilih semua kartu fitur
    const nextButton = document.querySelector('.next-button'); // Tombol "Next"
    const prevButton = document.querySelector('.prev-button'); // Tombol "Previous"
    let currentIndex = 0; // Indeks awal kartu aktif

    // Fungsi untuk memperbarui kartu aktif
    function updateActiveCard(index) {
        cards.forEach((card, i) => {
            if (i === index) {
                card.classList.add('active'); // Tambahkan kelas "active" untuk kartu aktif
            } else {
                card.classList.remove('active'); // Hapus kelas "active" untuk kartu lainnya
            }
        });
    }

    // Fungsi untuk menampilkan kartu berikutnya
    function showNextCard() {
        currentIndex = (currentIndex + 1) % cards.length; // Loop ke awal jika indeks mencapai akhir
        updateActiveCard(currentIndex);
    }

    // Fungsi untuk menampilkan kartu sebelumnya
    function showPrevCard() {
        currentIndex = (currentIndex - 1 + cards.length) % cards.length; // Loop ke akhir jika indeks di awal
        updateActiveCard(currentIndex);
    }

    // Tambahkan event listener ke tombol navigasi
    nextButton.addEventListener('click', showNextCard);
    prevButton.addEventListener('click', showPrevCard);

    // Slideshow otomatis setiap 5 detik
    setInterval(showNextCard, 5000);

    // Inisialisasi: Tampilkan kartu pertama saat halaman dimuat
    updateActiveCard(currentIndex);
});
