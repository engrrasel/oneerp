function showAccountInfo() {

    document
        .getElementById('accountModal')
        .classList.add('show');

}

function hideAccountInfo() {

    document
        .getElementById('accountModal')
        .classList.remove('show');

}

function copyAccountInfo() {

    const text = `
Account Name: ${window.walletAccountName || '-'}
Account Number: ${window.walletAccountNumber || '-'}
Bank: ${window.walletBankName || '-'}
Branch: ${window.walletBranchName || '-'}
`;

    if (navigator.clipboard && window.isSecureContext) {

        navigator.clipboard.writeText(text)
            .then(() => {
                showToast('Account information copied successfully.');
            })
            .catch(() => {
                fallbackCopy(text);
            });

    } else {

        fallbackCopy(text);

    }

}

function fallbackCopy(text) {

    const textarea = document.createElement('textarea');

    textarea.value = text;

    textarea.style.position = 'fixed';
    textarea.style.left = '-9999px';

    document.body.appendChild(textarea);

    textarea.focus();
    textarea.select();

    try {

        document.execCommand('copy');

        showToast('Account information copied successfully.');

    } catch (err) {

        showToast('Copy failed. Please copy manually.');

    }

    document.body.removeChild(textarea);

}

function showToast(message) {

    const toast = document.getElementById('toast');

    if (!toast) return;

    toast.querySelector('span').textContent = message;

    toast.classList.add('show');

    clearTimeout(toast.hideTimer);

    toast.hideTimer = setTimeout(() => {

        toast.classList.remove('show');

    }, 3000);

}