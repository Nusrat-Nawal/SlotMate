function openDeleteModal() {
    document.getElementById("modal").style.display = "flex";
}

function closeModal() {
    document.getElementById("modal").style.display = "none";
}

function deleteSelected() {

    let selected = [];

    document.querySelectorAll(".select-box:checked").forEach(cb => {
        selected.push(cb.value);
    });

    if (selected.length === 0) {
        alert("No requests selected!");
        return;
    }

    //send to backend
    window.location.href = "/delete-multiple/?ids=" + selected.join(",");

}