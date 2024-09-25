document.getElementById('profileDropdown').addEventListener('click', function(event) {
    event.preventDefault();
    var menu = document.getElementById('profileMenu');
    if (menu.style.display === 'none' || menu.style.display === '') {
        menu.style.display = 'block';
    } else {
        menu.style.display = 'none';
    }
});

// Cerrar el menú si se hace clic fuera de él
window.addEventListener('click', function(event) {
    var menu = document.getElementById('profileMenu');
    if (!event.target.matches('#profileDropdown, .profile-icon') && menu.style.display === 'block') {
        menu.style.display = 'none';
    }
});
