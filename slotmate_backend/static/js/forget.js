const emailInput = document.getElementById("email");
const sendBtn = document.getElementById("sendBtn");

emailInput.addEventListener("input", function () {

    let emailValue = emailInput.value.trim();

    if (
        emailValue.includes("@") &&
        emailValue.includes(".")
    ) {

        sendBtn.disabled = false;
        sendBtn.classList.remove("disabled");

    } else {

        sendBtn.disabled = true;
        sendBtn.classList.add("disabled");
    }

});

sendBtn.addEventListener("click", function () {

    alert("Verification code sent to your email!");

});

if (valid) {

      window.location.href = "../login.html";
}
