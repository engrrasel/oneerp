const sidebar =
    document.getElementById('sidebar');

const overlay =
    document.getElementById('overlay');

function toggleSidebar(e) {

    if (e) {
        e.stopPropagation();
    }

    if (window.innerWidth <= 768) {

        sidebar.classList.toggle('show');

        if (overlay) {
            overlay.classList.toggle('active');
        }

    } else {

        sidebar.classList.toggle('collapsed');
    }
}

if (overlay) {

    overlay.addEventListener(
        'click',
        function () {

            sidebar.classList.remove('show');
            overlay.classList.remove('active');

        }
    );
}