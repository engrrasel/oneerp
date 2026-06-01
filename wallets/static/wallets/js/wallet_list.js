document.addEventListener('DOMContentLoaded', function () {


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

    wallets.forEach(function (wallet) {

        const option =
            document.createElement('option');

        option.value =
            wallet.id;

        option.textContent =
            wallet.name;

        select.appendChild(option);

    });

}

function updateWalletInfo() {

    const card =
        document.getElementById(
            'from_wallet_info'
        );

    if (!card) {
        return;
    }

    const selectedId =
        fromWallet.value;

    const allWallets = [
        ...personalWallets,
        ...businessWallets
    ];

    const wallet =
        allWallets.find(function (w) {

            return String(w.id) ===
                String(selectedId);

        });

    if (!wallet) {

        card.style.display = 'none';
        return;

    }

    document.getElementById(
        'from_account_no'
    ).textContent =
        wallet.account_number || '-';

    document.getElementById(
        'from_balance'
    ).textContent =
        '৳' + wallet.balance;

    card.style.display =
        'block';

}

function updateWallets() {

    const type =
        transferType.value;

    if (type === 'pp') {

        fillSelect(
            fromWallet,
            personalWallets
        );

        fillSelect(
            toWallet,
            personalWallets
        );

    } else if (type === 'pb') {

        fillSelect(
            fromWallet,
            personalWallets
        );

        fillSelect(
            toWallet,
            businessWallets
        );

    } else if (type === 'bb') {

        fillSelect(
            fromWallet,
            businessWallets
        );

        fillSelect(
            toWallet,
            businessWallets
        );

    } else if (type === 'bp') {

        fillSelect(
            fromWallet,
            businessWallets
        );

        fillSelect(
            toWallet,
            personalWallets
        );

    }

    updateWalletInfo();

}

transferType.addEventListener(
    'change',
    updateWallets
);

fromWallet.addEventListener(
    'change',
    updateWalletInfo
);

updateWallets();


});
