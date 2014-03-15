
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

sonus.updateWidget = function (track_url, title, genre,valId) {

    if (sonus.userId != null) {

        
        SC.oEmbed(track_url, {auto_play: false}, function (oEmbed) {
            $("#"+valId).html(oEmbed.html);
        });

        sonus.getLocation(function (position) {
            $.ajax({
                url: "/song",
                type: "POST",
                data: {
                    latitude: position.coords.latitude,
                    longitude: position.coords.longitude,
                    songId: title,
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
                    songId: title,
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
      
      itemSelector: '.item'
    });

    SC.get('/tracks', {q: queryTerm}, function(tracks) {
        tracks.map(function (val) {
            if (val.artwork_url==null){
            val.artwork_url=val.user.avatar_url;
            if (val.artwork_url.indexOf('default_avatar_') == -1 ){
            val.artwork_url=val.artwork_url.replace("large","original");
            }
            
            }
            else{
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
                '"><img class="album" onerror="imgError('+val.id+')" src=' + val.artwork_url.replace("large","original") +
                '><span class="albumTitle">'+val.title+'</span> </div>'
                
                

                
            ).hide();
			$("#resultsTable").fadeIn('slow');
            $("#" + val.id).click(function(event) {
                console.log(event);
                sonus.updateWidget(
                    event.currentTarget.dataset.track_url,
                    event.currentTarget.dataset.title,
                    event.currentTarget.dataset.genre,
                    val.id
                );
            });
        });
    });
    $('#resultsTable').click()
    $('#resultsTable').css('position','static');
}

 function imgError(valId){
        $("#"+valId).remove();
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

    $(document).ready(function () {
        $("#logo").hide();
    $("#logo").fadeIn(2000);
        $("#intro").hide();
    $("#intro").fadeIn(2000);

    $(".item").on('click', function (event) {
                    alert(event.target.id);

        
    });
});
