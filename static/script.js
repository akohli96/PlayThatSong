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
    var xhr = new XMLHttpRequest(); //XML HTTP Request

    //xhr.open("GET", API + stuff, false);
    //xhr.setRequestHeader('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36')
    //xhr.setRequestHeader('Access-Control-Allow-Origin', '*');
    //xhr.setRequestHeader('Accept', 'application/json');
    //xhr.setRequestHeader('Host', 'api.genius.com')
    //xhr.setRequestHeader('Authorization', 'Bearer 7e-MLnwd98C0hxessa9wg5vxNWd0ib8T6T7wHiI__WyDNESmqp89_lxGZdBmToLg');
    //console.log(stuff);
    //xhr.send();

    //xhr.send();

    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                // Success! Do stuff with data.
                //console.log(xhr.responseText);
                var song_payload = xhr.response;
                var json = JSON.parse(song_payload);
                console.log(json);
            }
        }
    };

}