function keepAlive() {
    var refreshCookie = this.readCookie("medex_do_not_refresh");
    if (!refreshCookie) {
        console.log("refreshing tokens")
        this.refreshTokens();
    }
}

function refreshTokens() {
    $.ajax({
        url: "login-refresh",
        dataType: "json",
        method: "POST",
        context: document.body
    });
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

function getRefreshRate() {
    var refreshTokensSeconds = $('#refresh-tokens-period');

    if (refreshTokensSeconds.length > 0) {
        return parseInt(refreshTokensSeconds[0].value);
    } else {
        return 60 * 10;
    }
}

function runKeepAliveOnThisPage() {
    return $('#do-not-refresh-tokens').length === 0
}

function startKeepAlive() {
    var refreshTokensSeconds = getRefreshRate();
    if (runKeepAliveOnThisPage()) {
        keepAlive();
        setInterval(keepAlive, refreshTokensSeconds * 300);
    }
}

$(document).ready(function () {
    startKeepAlive();
});

