// Function to show settings sections
function showSection(sectionId) {
    // Hide all sections
    var sections = document.getElementsByClassName('settings-section');
    for (var i = 0; i < sections.length; i++) {
        sections[i].classList.remove('active');
    }
    // Show the selected section
    document.getElementById(sectionId).classList.add('active');
}

// Function to change theme and save the choice
function changeTheme() {
    var theme = document.getElementById('theme').value;

    if (theme === 'dark') {
        document.body.classList.add('dark-mode');
        document.body.classList.remove('light-mode');
        localStorage.setItem('theme', 'dark'); // Save the choice to localStorage
    } else {
        document.body.classList.add('light-mode');
        document.body.classList.remove('dark-mode');
        localStorage.setItem('theme', 'light'); // Save the choice to localStorage
    }
}

// Load the theme on page load
document.addEventListener('DOMContentLoaded', function () {
    var savedTheme = localStorage.getItem('theme'); // Retrieve the saved theme from localStorage

    if (savedTheme === 'dark') {
        document.body.classList.add('dark-mode');
        document.body.classList.remove('light-mode');
        document.getElementById('theme').value = 'dark'; // Set dropdown to dark
    } else {
        document.body.classList.add('light-mode');
        document.body.classList.remove('dark-mode');
        document.getElementById('theme').value = 'light'; // Set dropdown to light
    }
});
