const walletType =
    document.getElementById('walletType');

const bankFields =
    document.getElementById('bankFields');

const mobileFields =
    document.getElementById('mobileFields');

function toggleFields(){

    bankFields.style.display = 'none';
    mobileFields.style.display = 'none';

    if(walletType.value === 'bank'){
        bankFields.style.display = 'block';
    }

    if(walletType.value === 'mobile_banking'){
        mobileFields.style.display = 'block';
    }

}

walletType.addEventListener(
    'change',
    toggleFields
);

toggleFields();