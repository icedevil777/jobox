function show_hide_password(target){
    var input = document.getElementById('pxp-signup-password');
    var input2 = document.getElementById('pxp-signup-password-repeat');

    if (input.getAttribute('type') == 'password') {
        target.classList.add('view');
        input.setAttribute('type', 'text');
        input2.setAttribute('type', 'text');
    } else {
        target.classList.remove('view');
        input.setAttribute('type', 'password');
        input2.setAttribute('type', 'password');
    }
    return false;
}

function show_hide_pass(target){
    var input = document.getElementById('pxp-signin-page-password');
    if (input.getAttribute('type') == 'password') {
        target.classList.add('view');
        input.setAttribute('type', 'text');
    } else {
        target.classList.remove('view');
        input.setAttribute('type', 'password');
    }
    return false;
}