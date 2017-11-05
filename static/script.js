var stuff;
var artist;
var title;
var videoid;

function getSong(lyrics) {
    var lyrics_xhr = new XMLHttpRequest();
    var url = '/api/search';
    lyrics_xhr.open("POST", url, true);
    lyrics_xhr.setRequestHeader("Content-type", "application/json");
    console.log("hello world");
    lyrics_xhr.onreadystatechange = function() {
        if (lyrics_xhr.readyState === 4) {
            if (lyrics_xhr.status === 200) {
                var song_payload = lyrics_xhr.response;
                var json = JSON.parse(song_payload);
                console.log(json)
                artist = json['0']['artist']
                title = json['0']['title']
                getVideoUrl();
            }
        }
    };
    lyrics_xhr.send(JSON.stringify({ 'search': lyrics  }));
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
            var videoURL = json['0']
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

function loadVideo(video){
  stopVideo();

  done = false;
  if(videoid != video ){
    player.loadVideoById(videoid, 0, "large")
  }
  startDictation();
}


/***SPEECH DICTATION ****/

function startDictation() {

    if (window.hasOwnProperty('webkitSpeechRecognition')) {
        console.log("Starting");
        var recognition = new webkitSpeechRecognition();

        recognition.continuous = false;
        recognition.interimResults = false;

        recognition.lang = "en-US";
        recognition.start();
        console.log("After Start");
        recognition.onresult = function(e) {
            console.log("Found Something")
            var transcript = e.results[0][0].transcript;
            recognition.stop();
            getSong(transcript)
        };

        recognition.onerror = function(e) {
            recognition.stop();
        }

    }
}

startDictation()
