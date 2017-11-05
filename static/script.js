var stuff;
var artist;
var title;

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
                artist = json['0']['artist']
                title = json['0']['title']
            }
        }
    };
    lyrics_xhr.send(JSON.stringify({ 'search': stuff }));
}

//gettig video url
function getVideoUrl(){
  var video_xhr = new XMLHttpRequest();
  var url = '/api/video'
  video_xhr.open("POST", url, true)
  video_xhr.setRequestHeader("Content-type", "application/json");
  video_xhr.onreadystatechange = function() {
    if (video_xhr.readyState === 4) {
        if (video_xhr.status === 200) {
            var json = JSON.parse(video_xhr.response)
            var videoURL = json['0'].substring(json['0'].indexOf("=") + 1)
            loadVideo(videoURL);
          }
    }
  }
  var stuff = artist + " " + title
  console.log(stuff)
  video_xhr.send(JSON.stringify({ 'search':  stuff }));
}

// Youtube Video loading
var tag = document.createElement("script")

tag.src = "https://www.youtube.com/iframe_api"
var firstScriptTag = document.getElementsByTagName('script')[0]
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

var player;
function onYouTubeIframeAPIReady(){
  player = new YT.Player('player', {
    height: '390',
    width: '640',
    videoId: 'M7lc1UVf-VE',
    events: {
      'onReady': onPlayerReady,
      'onStateChange': onPlayerStateChange
    }
  })
}

var onPlayerReady = function(event){
  event.target.playVideo();
}

var done = false;
var onPlayerStateChange = function(){

}
var stopVideo = function(){
  if(player != null){
    player.stopVideo()
  }
}

function loadVideo(videoid){
  stopVideo();

  done = false;
  console.log(videoid)
  player.loadVideoById(videoid, 0, "large ")
}
