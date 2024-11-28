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

function changeTheme() {
    var theme = document.getElementById('theme').value;
    if (theme == 'dark') {
        document.body.classList.add('dark-mode');
        document.body.classList.remove('light-mode');
    } else {
        document.body.classList.add('light-mode');
        document.body.classList.remove('dark-mode');
    }
}

document.addEventListener('DOMContentLoaded', function() {
    var theme = 'light';
    if (theme == 'dark') {
        document.body.classList.add('dark-mode');
    } else {
        document.body.classList.remove('light-mode')
    }
})