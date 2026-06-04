function validatePassword(input) {
    input.value = input.value.replace(/[^a-zA-Z0-9]/g, '');
    if (input.value.length > 8) {
        input.value = input.value.slice(0, 8);
    }
}