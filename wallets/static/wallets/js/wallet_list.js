document.addEventListener('DOMContentLoaded', function () {

    setTimeout(function () {

        const alerts =
            document.querySelectorAll('.auto-dismiss-alert');

        alerts.forEach(function(alert){

            alert.style.transition =
                'all .4s ease';

            alert.style.opacity = '0';
            alert.style.transform =
                'translateY(-10px)';

            setTimeout(function(){
                alert.remove();
            }, 400);

        });

    }, 3000);

});