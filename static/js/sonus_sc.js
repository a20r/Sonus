
var sonus = sonus || {};

sonus.greedyQuery = function (queryTerm) {
    SC.get('/tracks', {q: queryTerm}, function(tracks) {
        var track_url = tracks[0].permalink_url;
        SC.oEmbed(track_url, {auto_play: false}, function(oEmbed) {
            $("#widget").html(oEmbed.html);
        });
    });
}

sonus.init = function() {
    SC.initialize({
      client_id: '0020643627fb540d480f7c4434796d2c'
    });

    $("#searchButton").click(function () {
        sonus.greedyQuery($("#query").val());
        console.log("here");
    });
}

window.onload = sonus.init;

