var idleMinutes = 0;
var maxIdleMinutes = 60;

function timerIncrement() {
    idleMinutes = idleMinutes + 1;
    if (idleMinutes >= maxIdleMinutes) { // 60 minutes
        window.location = '/logout';
    }
}

function startWatchers() {
    //Increment the idle time counter every minute.
    setInterval(timerIncrement, 60000); // 1 minutes

    //Zero the idle timer on mouse movement.
    $(this).mousemove(function (e) {
        idleMinutes = 0;
    });
    $(this).keypress(function (e) {
        idleMinutes = 0;
    });
}

function getVariables() {
    var maxSecondsHiddenInput = $('#max-idle-seconds');
    if(maxSecondsHiddenInput.length > 0) {
        var maxSeconds = parseInt(maxSecondsHiddenInput[0].value);
        maxIdleMinutes = maxSeconds/60
    }
}

function runIdleLogoutOnThisPage() {
    return $('#do-not-refresh-tokens').length == 0
}

$(document).ready(function () {
    getVariables();
    if (runIdleLogoutOnThisPage()) {
        startWatchers()
    }
});