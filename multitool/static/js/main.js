function initTheme() {
    theme = window.localStorage.getItem('data-theme');
    if(theme) {
        document.body.setAttribute('data-theme', theme);
    } else {
        window.localStorage.setItem('data-theme', 'dark');
        document.body.setAttribute('data-theme', 'dark');
    }

    if (theme === 'dark') {
        document.getElementById("themeToggle").checked = true;
    } else {
        document.getElementById("themeToggle").checked = false;
    }
}

initTheme();

const darkButton = document.getElementById('dark');
const lightButton = document.getElementById('light');

/* $('#nav_img').click(function(){

}) */

/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
function userDropdown() {
    document.getElementById("user_dropdown").classList.toggle("show");
}

// Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
    if (!event.target.matches('#nav_img') && !event.target.matches('#user_dropdown')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        var i;
        for (i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}

// darkButton.onclick = () => {
//     // body.classList.remove('light');
//     // body.classList.add('dark');
//     document.body.setAttribute('data-theme', 'dark');
//     window.localStorage.setItem('data-theme', 'dark');
// }

// lightButton.onclick = () => {
//     // body.classList.remove('dark');
//     // body.classList.add('light');
//     document.body.setAttribute('data-theme', 'light');
//     window.localStorage.setItem('data-theme', 'light');
// }

function toggleTheme() {
    theme = window.localStorage.getItem('data-theme');
    if(theme) {
        if (theme === 'light') {
            document.body.setAttribute('data-theme', 'dark');
            window.localStorage.setItem('data-theme', 'dark');
        } else if (theme === 'dark') {
            document.body.setAttribute('data-theme', 'light');
            window.localStorage.setItem('data-theme', 'light');
        } else {
            console.log("Unknown theme");
        }
    }
}