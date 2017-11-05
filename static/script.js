var stuff;
document.querySelector('#button').onclick = function() {
    fetch('/api/speech-to-text/token')
        .then(function(response) {
            return response.text();
        }).then(function(token) {

            var stream = WatsonSpeech.SpeechToText.recognizeMicrophone({
                token: token,
                object_mode: false
            });

            stream.setEncoding('utf8'); // get text instead of Buffers for on data events

            stream.on('data', function(data) {
                stuff = data;
                console.log(stuff);
            });

            stream.on('error', function(err) {
                console.log(err);
            });

            document.querySelector('#stop').onclick = stream.stop.bind(stream);

        }).catch(function(error) {
            console.log(error);
        });
};

function getSong() {
    var lyrics_xhr = new XMLHttpRequest();
    var url = '/api/search';
    lyrics_xhr.open("POST", url, true);
    lyrics_xhr.setRequestHeader("Content-type", "application/json");
    lyrics_xhr.onreadystatechange = function() {
        if (lyrics_xhr.readyState === 4) {
            if (lyrics_xhr.status === 200) {
                var song_payload = lyrics_xhr.response;
                var json = JSON.parse(song_payload);
                console.log(json);
            }
        }
    };
    lyrics_xhr.send(JSON.stringify({ 'search': stuff }));

}