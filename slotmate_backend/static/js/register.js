let generatedCode = "";
let verified = false;
function registerUser() {

  
  let firstName = document.querySelector("input[placeholder='Rafiq']").value;
  let email = document.querySelector("input[type='email']").value;
  let department = document.getElementById("department").value;
  let studentId = document.querySelector("input[placeholder='2021200000']").value;
  let password = document.getElementById("password").value;
  let confirmPassword = document.getElementById("confirmPassword").value;

  let university = document.querySelector("select").value;

  
  let nameError = document.getElementById("nameError");
  let emailError = document.getElementById("emailError");
  let deptError = document.getElementById("DeptError");
  let idError = document.getElementById("idError");
  let selectError = document.getElementById("selectError");
  let verifyError = document.getElementById("verifyError");

  let enteredCode = document.getElementById("verificationCode").value;

  let termsCheck = document.getElementById("termsCheck");

  
  nameError.innerText = "";
  emailError.innerText = "";
  deptError.innerText = "";
  idError.innerText = "";
  selectError.innerText = "";
  verifyError.innerText = "";

  let valid = true;


  if (firstName.trim() === "") {
    nameError.innerText = "Please enter your name";
    valid = false;
  }

  if (email.trim() === "") {
    emailError.innerText = "Please enter your email";
    valid = false;
  }

  if (department.trim() === "") {
    deptError.innerText = "Please enter your department";
    valid = false;
  }

  if (studentId.trim() === "") {
    idError.innerText = "Please enter your student ID";
    valid = false;
  }

  if (university === "" || university === "Select your university") {
    selectError.innerText = "Please select your university";
    valid = false;
  }

  let passError = document.getElementById("passError");
let confirmPassError = document.getElementById("confirmPassError");

passError.innerText = "";
confirmPassError.innerText = "";

if (password.trim() === "") {
  passError.innerText = "Please enter your password";
  valid = false;
}
else if (password.length !== 8) {
  passError.innerText = "Password must be exactly 8 characters";
  valid = false;
}

if (confirmPassword.trim() === "") {
  confirmPassError.innerText = "Please confirm password";
  valid = false;
}

if (password !== confirmPassword) {
  confirmPassError.innerText = "Passwords do not match";
  valid = false;
}
if (generatedCode === "") {
  verifyError.innerText = "Please send verification code";
  valid = false;
}

else if (enteredCode !== generatedCode) {
  verifyError.innerText = "Incorrect verification code";
  valid = false;
}

if (!termsCheck.checked) {
  alert("Please accept Terms & Conditions");
  valid = false;
}
  
  if (valid) {
    
   window.location.href = "../index.html";
  }
}
function sendCode() {
    let email = document.querySelector("input[name='email']").value;

    if (email.trim() === "") {
        document.getElementById("emailError").innerText = "Please enter your email first";
        return;
    }
    if (!email.endsWith(".edu") && !email.includes(".edu.")) {
        document.getElementById("emailError").innerText = "Please use your university email (.edu)";
        return;
    }

    fetch("/send-verification/", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: "email=" + encodeURIComponent(email)
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === "success") {
            alert("Verification code sent to your email!");
        } else {
            alert("Failed: " + data.message);
        }
    })
    .catch(err => {
        alert("Email send failed. Check your internet connection.");
    });
}
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
function validatePassword(input) {
      input.value = input.value.replace(/[^a-zA-Z0-9]/g, '');
      if (input.value.length > 8) {
        input.value = input.value.slice(0, 8);
      }
}
function clearError(id) {
  document.getElementById(id).innerText = "";
}
  
