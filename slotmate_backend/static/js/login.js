const emailInput = document.getElementById("loginEmail");
const passwordInput = document.getElementById("loginPassword");

const emailError = document.getElementById("loginEmailError");
const passError = document.getElementById("loginPassError");


// remove email and password error while typing
emailInput.addEventListener("input", function () {

    if (emailInput.value.trim() !== "") {
        emailError.innerText = "";
    }

});



passwordInput.addEventListener("input", function () {

    if (passwordInput.value.trim() !== "") {
        passError.innerText = "";
    }

});



function loginUser() {

    let valid = true;

    emailError.innerText = "";
    passError.innerText = "";

    if (emailInput.value.trim() === "") {

        emailError.innerText = "Please enter your username/email";
        valid = false;
    }

    if (passwordInput.value.trim() === "") {

        passError.innerText = "Please enter your password";
        valid = false;
    }

    if (valid) {

      window.location.href = "../index.html";
    }
}