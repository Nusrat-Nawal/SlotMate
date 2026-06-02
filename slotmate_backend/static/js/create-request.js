let currentDays = [];
let previousPreferredTime = "";

function toggleCurrentDay(el, value){

    el.classList.toggle("active");

    if(currentDays.includes(value)){
        currentDays = currentDays.filter(d => d !== value);
    } else {
        currentDays.push(value);
    }

    document.getElementById("currentDay").value = currentDays.join(",");
}

let preferredDays = [];

function togglePreferredDay(el,value){

    el.classList.toggle("active");

    if(preferredDays.includes(value)){
        preferredDays = preferredDays.filter(d => d !== value);
    } else {
        preferredDays.push(value);
    }

    document.getElementById("preferredDay").value = preferredDays.join(",");
}

function selectCurrentTime(el,value){

    document.querySelectorAll("#currentTimeGroup .chip")
    .forEach(c => c.classList.remove("active"));

    el.classList.add("active");
    document.getElementById("currentTime").value = value;
}

function selectPreferredTime(el,value){

    document.querySelectorAll("#preferredTimeGroup .chip")
    .forEach(c => c.classList.remove("active"));

    el.classList.add("active");
    document.getElementById("preferredTime").value = value;
    previousPreferredTime = value;
}
//For Any Options

//For any faculty option
let previousFaculty = "";
const anyFaculty = document.getElementById("anyFaculty");

if (anyFaculty) {
      anyFaculty.addEventListener("change", function () {

        const input = document.getElementById("preferredFaculty");
        if (!input) return;

        if (this.checked) {
            previousFaculty = input.value;
            input.value = "";
            input.disabled = true;
            input.style.opacity = "0.4";
        } else {
            input.value = previousFaculty;
            input.disabled = false;
            input.style.opacity = "1";
        }
    });
}

//For any day option
const anyDay = document.getElementById("anyDay");
const preferredDayGroup = document.getElementById("preferredDayGroup");

if (anyDay && preferredDayGroup) {
anyDay.addEventListener("change", function () {

    const chips = preferredDayGroup.querySelectorAll(".chip");
    if (this.checked) {
        currentDays = [];
        preferredDays = [];
        document.getElementById("preferredDay").value = "";
        document.querySelectorAll("#preferredDayGroup .chip, #currentDayGroup .chip")
         .forEach(c => c.classList.remove("active"));

        chips.forEach(c => {
            c.classList.remove("active");
            c.style.pointerEvents = "none";
        });

        preferredDayGroup.style.opacity = "0.4";
    } else {
        chips.forEach(c => c.style.pointerEvents = "auto");
        preferredDayGroup.style.opacity = "1";
    }

} ); } 

const anyTime = document.getElementById("anyTime");
const preferredTimeGroup = document.getElementById("preferredTimeGroup");

if (anyTime && preferredTimeGroup) {
anyTime.addEventListener("change", function () {

    const chips = preferredTimeGroup.querySelectorAll(".chip");
    if (this.checked) {
        previousPreferredTime = document.getElementById("preferredTime").value;

        document.getElementById("preferredTime").value = "";

        chips.forEach(c => {
            c.classList.remove("active");
            c.style.pointerEvents = "none";
        });

        preferredTimeGroup.style.opacity = "0.4";
    } else {
        document.getElementById("preferredTime").value = previousPreferredTime;
        chips.forEach(c => c.style.pointerEvents = "auto");
        preferredTimeGroup.style.opacity = "1";
    }

} ) ; } 

const anySection = document.getElementById("anySection");
    if (anySection) {
    anySection.addEventListener("change", function () {

        const input = document.getElementById("preferredSection");

        if (!input) return;

        if (this.checked) {
            input.value = "";
            input.disabled = true;
            input.style.opacity = "0.4";
        } else {
            input.disabled = false;
            input.style.opacity = "1";
        }
    });
}

document.addEventListener("DOMContentLoaded", function (){
    const popup = document.getElementById("policyPopup");
    if (popup && !localStorage.getItem("hideRequestPolicy")) {
        popup.classList.remove("hidden");
    }
});

window.acceptPolicy = function () {
    const dontShow = document.getElementById("dontShowAgain");

    if (dontShow && dontShow.checked) {
        localStorage.setItem("hideRequestPolicy", "true");
    }

    const popup = document.getElementById("policyPopup");
    if (popup) {
        popup.classList.add("hidden");
    }
};

document.addEventListener("DOMContentLoaded", function () {
    const btn = document.getElementById("acceptBtn");

    if (btn) {
        btn.addEventListener("click", function () {
            window.acceptPolicy();
        });
    }
});