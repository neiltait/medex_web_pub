var idleMinutes = 0;
var maxIdleMinutes = 60;
var userIsIdle = true;

function startIdleTimer() {
    resetCookie()

    //Increment the idle time counter every minute.
    setInterval(update, 60000); // 1 minutes

    //Zero the idle timer on mouse movement.
    $(this).mousemove(function (e) {
        userIsIdle = false;
    });
    $(this).keypress(function (e) {
        userIsIdle = false;
    });
}

function update() {
    if (userIsIdle) {
        logoutIfMaxTimeExceeded()
    } else {
        resetCookie()
    }
}

function logoutIfMaxTimeExceeded() {
    if (cookieHasTimedOut()) {
        window.location = '/logout';
    }
}

function resetCookie() {
    createCookie("medex_logged_in", "logged in", maxIdleMinutes)
}

function cookieHasTimedOut() {
    return readCookie("medex_logged_in") === null
}

function createCookie(name, value, minutes) {
    if (minutes) {
        var date = new Date();
        date.setTime(date.getTime() + (minutes * 60 * 1000));
        var expires = "; expires=" + date.toGMTString();
    } else {
        var expires = "";
    }
    document.cookie = name + "=" + value + expires + "; path=/";
}

function readCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

function getVariables() {
    var maxSecondsHiddenInput = $('#max-idle-seconds');
    if (maxSecondsHiddenInput.length > 0) {
        var maxSeconds = parseInt(maxSecondsHiddenInput[0].value);
        maxIdleMinutes = maxSeconds / 60
    }
}

function runIdleLogoutOnThisPage() {
    return $('#do-not-refresh-tokens').length == 0
}

$(document).ready(function () {
    getVariables();
    if (runIdleLogoutOnThisPage()) {
        startIdleTimer()
    }
});