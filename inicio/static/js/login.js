function togglePasswordVisibility() {
    const passwordInput = document.getElementById("password");
    const eyeIcon = document.querySelector(".eye i");
    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        eyeIcon.className = "fa-solid fa-eye-slash";
    } else {
        passwordInput.type = "password";
        eyeIcon.className = "fa-solid fa-eye"
    }
}