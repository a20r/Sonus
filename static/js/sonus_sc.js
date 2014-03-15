
var sonus = sonus || {};

sonus.greedyQuery = function (queryTerm) {
    SC.get('/tracks', {q: queryTerm}, function(tracks) {
        var track_url = tracks[0].permalink_url;
        SC.oEmbed(track_url, {auto_play: false}, function(oEmbed) {
            $("#widget").html(oEmbed.html);
        });
    });
}

sonus.updateWidget = function (track_url) {
    SC.oEmbed(track_url, {auto_play: false}, function (oEmbed) {
        $("#widget").html(oEmbed.html);
    });
}

sonus.scQuery = function (queryTerm) {
    $("#resultTable").html("");
    SC.get('/tracks', {q: queryTerm}, function(tracks) {
        tracks.map(function (val) {
            $("#resultTable").append(
                "<tr onclick=sonus.updateWidget(\'" +
                val.permalink_url + "\')><td>" + val.title + "</td></tr>"
            );
        });
    });

}

sonus.init = function () {
    SC.initialize({
        client_id: '0020643627fb540d480f7c4434796d2c'
    });

    $("#searchButton").click(function () {
        sonus.scQuery($("#query").val());
        console.log("here");
    });
}

// Sets the locaction event handlers
sonus.getLocation = function () {
    if (navigator.geolocation) {
        var timeoutVal = 6000;

        var extraGeoParam = {
            enableHighAccuracy: true,
            timeout: timeoutVal,
            maximumAge: 0
        };

        navigator.geolocation.watchPosition(
            devicePositionHandler,
            positionError,
            extraGeoParam
        );
    } else {
        alert("Geolocation is not supported by this browser");
    }
}

sonus.positionError = function (position) {
    console.log("error");
}

sonus.devicePositionHandler = function (position) {
    console.log(position.coords.latitude);
    console.log(position.coords.longitude);
}

window.onload = sonus.init;

