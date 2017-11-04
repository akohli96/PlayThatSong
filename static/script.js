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