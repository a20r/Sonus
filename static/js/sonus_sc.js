
var sonus = sonus || {};

sonus.userId = null;

sonus.greedyQuery = function (queryTerm) {
    SC.get('/tracks', {q: queryTerm}, function(tracks) {
        var track_url = tracks[0].permalink_url;
        SC.oEmbed(track_url, {auto_play: false}, function(oEmbed) {
            $("#widget").html(oEmbed.html);
        });
    });
}

sonus.updateWidget = function (track_url, title, genre) {

    if (sonus.userId != null) {
        SC.oEmbed(track_url, {auto_play: false}, function (oEmbed) {
            $("#widget").html(oEmbed.html);
        });

        sonus.getLocation(function (position) {
            $.ajax({
                url: "/song",
                type: "POST",
                data: {
                    latitude: position.coords.latitude,
                    longitude: position.coords.longitude,
                    title: title,
                    genre: genre,
                    userId: sonus.userId
                }
            });
        }, function (position) {
            $.ajax({
                url: "/song",
                type: "POST",
                data: {
                    latitude: null,
                    longitude: null,
                    title: title,
                    genre: genre,
                    userId: sonus.userId
                }
            });
        });
    } else {
        alert("You are not logged in: Ammaar will make this pretty");
    }

}

sonus.scQuery = function (queryTerm) {
    $("#resultsTable").html("");
    SC.get('/tracks', {q: queryTerm}, function(tracks) {
        tracks.map(function (val) {
            $("#resultsTable").append(
                "<tr onclick=\'sonus.updateWidget(\"" + val.permalink_url + "\", \"" +
                val.title + "\", \"" + val.genre + "\")\'><td>" +
                val.title + "</td></tr>"
            );
        });
    });
}

sonus.init = function () {
    SC.initialize({
        client_id: '0020643627fb540d480f7c4434796d2c'
    });

    $("#form").on("submit", function () {
        sonus.scQuery($("#query").val());
        $("#query").val("");
        return false;
    });
}

// Sets the locaction event handlers
sonus.getLocation = function (onSuccess, onError) {
    if (navigator.geolocation) {
        var timeoutVal = 6000;

        var extraGeoParam = {
            enableHighAccuracy: true,
            timeout: timeoutVal,
            maximumAge: 0
        };

        navigator.geolocation.getCurrentPosition(
            onSuccess,
            onError,
            extraGeoParam
        );
    } else {
        alert("Geolocation is not supported by this browser");
    }
}

window.onload = sonus.init;

