document.addEventListener('DOMContentLoaded', function () {

    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('overlay');
    const menuBtn = document.getElementById('mobileMenuBtn');

    function toggleSidebar() {

        if (!sidebar) return;

        sidebar.classList.toggle('show');

        if (overlay) {
            overlay.classList.toggle('active');
        }
    }

    if (menuBtn) {

        menuBtn.addEventListener('click', function (e) {

            e.preventDefault();
            e.stopPropagation();

            console.log('Mobile menu clicked');

            toggleSidebar();

        });

    }

    if (overlay) {

        overlay.addEventListener('click', function () {

            sidebar.classList.remove('show');
            overlay.classList.remove('active');

        });

    }

    window.toggleSidebar = function (e) {

        if (e) e.stopPropagation();

        if (window.innerWidth <= 768) {

            toggleSidebar();

        } else {

            sidebar.classList.toggle('collapsed');

        }

    };

});