const span = document.getElementById("name-text");

document.addEventListener("DOMContentLoaded", loadUsername)

async function loadUsername() {
    const response = await fetch("http://ardor/getUsername");
    const data = await response.text();
    span.textContent = data;
}

