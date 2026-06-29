document.addEventListener("DOMContentLoaded", function () {

    document.querySelectorAll(".bar").forEach(function (bar) {

        let width = bar.getAttribute("data-width");

        if (!width) {
            width = 0;
        }

        // safety clamp
        width = parseFloat(width);
        if (width > 100) width = 100;
        if (width < 0) width = 0;

        bar.style.width = width + "%";

    });

    document.querySelectorAll(".score-circle").forEach(el => {
    let text = el.innerText.replace("%","");
    el.style.setProperty("--score", text);
    });

});