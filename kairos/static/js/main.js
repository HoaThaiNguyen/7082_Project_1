console.log("main.js starts");

document.addEventListener("DOMContentLoaded", () => {
    const toggleButton = document.getElementById("menu-toggle");
    const dropdown = document.getElementById("dropdown-menu");

    toggleButton.addEventListener("click", () => {
        dropdown.classList.toggle("hidden");
    });

    // Optional: hide the dropdown if you click outside
    document.addEventListener("click", (event) => {
        if (!toggleButton.contains(event.target) && !dropdown.contains(event.target)) {
            dropdown.classList.add("hidden");
        }
    });
});

console.log("main.js ends");
