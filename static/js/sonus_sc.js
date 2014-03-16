
var sonus = sonus || {};

sonus.userId = null;
sonus.geocoder = null;

sonus.greedyQuery = function (queryTerm) {
    SC.get('/tracks', {q: queryTerm}, function(tracks) {
        var track_url = tracks[0].permalink_url;
        SC.oEmbed(track_url, {auto_play: false}, function(oEmbed) {
            $("#widget").html(oEmbed.html);
        });
    });
}

sonus.updateWidget = function (track_url, title, genre, valId) {

    if (sonus.userId != null) {
        SC.oEmbed(track_url, {auto_play: true}, function (oEmbed) {
            $("#" + valId).html(oEmbed.html);
            var valDiv = document.getElementById(valId);
            var frame = valDiv.getElementsByTagName("iframe")[0];
            var widget = SC.Widget(frame);
            widget.bind(SC.Widget.Events.FINISH, function () {
                $("#" + valId).next().click();
            });
        });

        sonus.getLocation(function (position) {
            $.ajax({
                url: "/song",
                type: "POST",
                data: {
                    latitude: position.coords.latitude,
                    longitude: position.coords.longitude,
                    songId: valId,
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
                    songId: valId,
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
     $('#resultsTable').html("")


    var $container = $('#resultsTable');
    $container.masonry({
      columnWidth: 200,
      itemSelector: '.item'
    });

    SC.get('/tracks', {q: queryTerm}, function(tracks) {
        tracks.map(sonus.manageTracks);
    });
    $('#resultsTable').click()
    $('#resultsTable').css('position','static');
}

sonus.manageTracks = function (val) {
    if (val.artwork_url==null){
        val.artwork_url=val.user.avatar_url;
        if (val.artwork_url.indexOf('default_avatar_') == -1 ){
            val.artwork_url=val.artwork_url.replace("large","original");
        }
    } else {
        val.artwork_url=val.artwork_url.replace("large","original");
    }
    if(val.artwork_url.indexOf('.jpg') == -1){
        val.artwork_url='/imgs/albumplaceholder.png';
    }
    $("#resultsTable").append(
        '<div class="item image" id="' +
        val.id+'" data-track_url="' +
        val.permalink_url + '" data-title="' + val.title +
        '" data-genre="' + val.genre +
        '"><img class="album" onerror="imgError('+val.id+')"src=' + val.artwork_url +
        '><span class="albumTitle">'+val.title+'</span> </div>'

    ).hide();
    $("#resultsTable").fadeIn('slow');
    $("#" + val.id).click(function(event) {
        sonus.updateWidget(
            event.currentTarget.dataset.track_url,
            event.currentTarget.dataset.title,
            event.currentTarget.dataset.genre,
            val.id
        );
    });
}

sonus.locationUpdateUI = function(lat, lng) {
    $.getJSON("/near/" + lat+ "/" + lng + "/5", function(json) {
            $('#resultsTable').html("");
            var $container = $('#resultsTable');
                $container.masonry({
                columnWidth: 200,
                itemSelector: '.item'
            });
            songs = json["songs"];
            songs.forEach(function(song) {
                SC.get("/tracks/" + song["songId"], function (scJson) {
                    sonus.manageTracks(scJson);
                });
            });
            $('#resultsTable').click()
            $('#resultsTable').css('position','static');
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

    $("#geoForm").on("submit", function () {
        sonus.geocodeUpdateUI($("#geocodeQuery").val());
        return false;
    });

    $("#nearMe").click(function () {
        sonus.getLocation(function (position) {
            sonus.locationUpdateUI(
                position.coords.latitude,
                position.coords.longitude
            );
        });
    });

    sonus.geocoder = new google.maps.Geocoder();
}

sonus.geocodeUpdateUI = function (addr) {
    sonus.geocoder.geocode({address: addr}, function (results, stat) {
        if (stat == google.maps.GeocoderStatus.OK) {
            sonus.locationUpdateUI(
                results[0].geometry.location.lat(),
                results[0].geometry.location.lng()
            );
        }
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

function imgError(valId){
    $("#"+valId).remove();
}
window.onload = sonus.init;

$(document).ready(function () {
    $("#introTitle").hide();
    $("#logo").hide();
    $("#logo").fadeIn(2000, function() {
        $("#logo").fadeOut(1000);
    });
    $("#intro").hide();
    $("#intro").fadeIn(2000, function() {
        $("#intro").fadeOut(1000, function() {
            $("#introTitle").fadeIn(1000);

            $("#nearMe").click();
        });
    });

    $(".item").on('click', function (event) {
        alert(event.target.id);
    });
});
