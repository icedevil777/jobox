let newPassword = document.querySelector('.new-password-js');
let verifyPassword = document.querySelector('.verify-password-js');
let noMatch = document.querySelector('.form__requirements--not-match');

verifyPassword?.addEventListener('blur', function () {
    if (newPassword.value !== verifyPassword.value) {
        noMatch.classList.add('show');
        verifyPassword.style.borderColor = "red";
    }
    else {
        noMatch.classList.remove('show');
        verifyPassword.style.borderColor = "";
    }
});