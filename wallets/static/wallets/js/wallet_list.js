document.addEventListener('DOMContentLoaded', function () {

    setTimeout(function () {

        const alerts =
            document.querySelectorAll('.auto-dismiss-alert');

        alerts.forEach(function (alert) {

            alert.style.transition =
                'all .4s ease';

            alert.style.opacity = '0';
            alert.style.transform =
                'translateY(-10px)';

            setTimeout(function () {
                alert.remove();
            }, 400);

        });

    }, 3000);

    const transferType =
        document.getElementById('transfer_type');

    const fromWallet =
        document.getElementById('send_from');

    const toWallet =
        document.getElementById('send_to');

    if (!transferType || !fromWallet || !toWallet) {
        return;
    }

    const personalWallets =
        window.personalWallets || [];

    const businessWallets =
        window.businessWallets || [];

    function fillSelect(select, wallets) {

        select.innerHTML =
            '<option value="">Select Wallet</option>';

        wallets.forEach(wallet => {

            select.innerHTML += `
                <option value="${wallet.id}">
                    ${wallet.name}
                </option>
            `;
        });
    }

    function updateWallets() {

        const type = transferType.value;

        if (type === 'pp') {

            fillSelect(fromWallet, personalWallets);
            fillSelect(toWallet, personalWallets);

        } else if (type === 'pb') {

            fillSelect(fromWallet, personalWallets);
            fillSelect(toWallet, businessWallets);

        } else if (type === 'bb') {

            fillSelect(fromWallet, businessWallets);
            fillSelect(toWallet, businessWallets);

        } else if (type === 'bp') {

            fillSelect(fromWallet, businessWallets);
            fillSelect(toWallet, personalWallets);

        }
    }

    transferType.addEventListener(
        'change',
        updateWallets
    );

    updateWallets();

});