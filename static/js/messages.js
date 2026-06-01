document.addEventListener('DOMContentLoaded', function () {

    const alerts = document.querySelectorAll('.custom-alert');

    alerts.forEach(function (alert) {

        const closeBtn = alert.querySelector('.alert-close');

        function removeAlert() {

            alert.classList.add('alert-hide');

            setTimeout(function () {
                alert.remove();
            }, 400);

        }

        if (closeBtn) {

            closeBtn.addEventListener('click', removeAlert);

        }

        setTimeout(removeAlert, 3000);

    });

});