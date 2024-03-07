function togglePasswordVisibility() {
    var passwordInput = document.querySelector('.password-field');
    var toggleIcon = document.querySelector('.toggle-password');
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        toggleIcon.classList.add('fa-eye-slash');
        toggleIcon.classList.remove('fa-eye');
    } else {
        passwordInput.type = 'password';
        toggleIcon.classList.remove('fa-eye-slash');
        toggleIcon.classList.add('fa-eye');
    }
}