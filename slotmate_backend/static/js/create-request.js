let currentDays = [];

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
}
//For Any Options

const anyFaculty = document.getElementById("anyFaculty");
const preferredFaculty = document.getElementById("preferredFaculty");

anyFaculty.addEventListener("change", function () {

    if (this.checked) {
        preferredFaculty.value = "";
        preferredFaculty.disabled = true;
        preferredFaculty.style.opacity = "0.4";
    } else {
        preferredFaculty.disabled = false;
        preferredFaculty.style.opacity = "1";
    }

  }
) ;

const anyDay = document.getElementById("anyDay");
const preferredDayGroup = document.getElementById("preferredDayGroup");

anyDay.addEventListener("change", function () {

    const chips = preferredDayGroup.querySelectorAll(".chip");
    if (this.checked) {
        document.getElementById("preferredDay").value = "";
        chips.forEach(c => c.style.pointerEvents = "none");
        preferredDayGroup.style.opacity = "0.4";
    } else {
        chips.forEach(c => c.style.pointerEvents = "auto");
        preferredDayGroup.style.opacity = "1";
    }

} ) ;

const anyTime = document.getElementById("anyTime");
const preferredTimeGroup = document.getElementById("preferredTimeGroup");

anyTime.addEventListener("change", function () {

    const chips = preferredTimeGroup.querySelectorAll(".chip");
    if (this.checked) {
        document.getElementById("preferredTime").value = "";
        chips.forEach(c => c.style.pointerEvents = "none");
        preferredTimeGroup.style.opacity = "0.4";
    } else {
        chips.forEach(c => c.style.pointerEvents = "auto");
        preferredTimeGroup.style.opacity = "1";
    }

} ) ;

const anySection = document.getElementById("anySection");
const preferredSection = document.getElementById("preferredSection");

anySection.addEventListener("change", function () {
    if (this.checked) {
        preferredSection.value = "";
        preferredSection.disabled = true;
        preferredSection.style.opacity = "0.4";
    } else {
        preferredSection.disabled = false;
        preferredSection.style.opacity = "1";
    }
} 
) ;