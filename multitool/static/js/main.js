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

/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
function userDropdown() {
    document.getElementById("user_dropdown").classList.toggle("show");
}

// Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
    var element = document.getElementById('user_dropdown');
    if (!event.target.matches('#nav_img') && (event.target !== element && !element.contains(event.target))) {
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