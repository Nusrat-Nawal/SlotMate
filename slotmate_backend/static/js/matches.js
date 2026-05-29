document.querySelectorAll(".bar").forEach(bar => {
    let width = bar.dataset.width || 0;

    width = Math.max(0, Math.min(100, parseFloat(width)));

    bar.style.width = width + "%";
});