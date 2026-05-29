document.addEventListener(
    'DOMContentLoaded',
    function(){

        const alerts =
        document.querySelectorAll(
            '.custom-alert'
        );

        alerts.forEach(function(alert){

            const closeBtn =
            alert.querySelector(
                '.alert-close'
            );

            if(closeBtn){

                closeBtn.addEventListener(
                    'click',
                    function(){

                        alert.classList.add(
                            'alert-hide'
                        );

                        setTimeout(
                            function(){

                                alert.remove();

                            },
                            400
                        );
                    }
                );
            }

            setTimeout(
                function(){

                    alert.classList.add(
                        'alert-hide'
                    );

                    setTimeout(
                        function(){

                            alert.remove();

                        },
                        400
                    );

                },
                3000
            );

        });

    }
);