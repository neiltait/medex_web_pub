var idleMinutes = 0;

function timerIncrement() {
    idleMinutes = idleMinutes + 1;
    if (idleMinutes >= 60) { // 60 minutes
        window.location = '/logout';
    }
}

function startWatchers() {
    //Increment the idle time counter every minute.
    setInterval(timerIncrement, 6000); // 1 minutes

    //Zero the idle timer on mouse movement.
    $(this).mousemove(function (e) {
        idleMinutes = 0;
    });
    $(this).keypress(function (e) {
        idleMinutes = 0;
    });
}


function runIdleLogoutOnThisPage() {
    return $('#do-not-refresh-tokens').length == 0
}

$(document).ready(function () {
    if (runIdleLogoutOnThisPage()) {
        startWatchers()
    }
});