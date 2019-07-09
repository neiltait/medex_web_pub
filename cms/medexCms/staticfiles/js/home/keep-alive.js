function keepAlive() {
    var refreshCookie = this.readCookie("medex_do_not_refresh");
    console.log("keeping alive");
    if (!refreshCookie) {
        console.log("refreshing");
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

function runKeepAliveOnThisPage() {
    return $('#do-not-refresh-tokens').length == 0
}
function startKeepAlive() {
    if(runKeepAliveOnThisPage()) {
        keepAlive();
        setInterval(keepAlive, 5*60*1000);
    }
}

startKeepAlive();
