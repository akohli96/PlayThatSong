
# PlayThatSong

Inspired by Shazam and simply forgetfulness!

Ever forget a song but know some of the lyrics? PlayThatSong uses the lyrics of the song the user sings to it to pull up a corresponding YouTube video. PlayThatSong was built under **24 hours** at [HackSI 2017](https://hacksi.org/)

Built by:
* [Ayush Kohli](github.com/akohli96)
* [Alec Waichunas](https://github.com/AlecWaichunas)



## TechStack
Backend : Python Flask

Frontend : HTML, CSS and JavaScript

Key API's:

* Web Speech API
* Youtube Data API
* tswift


## Getting started
```bash
git clone https://github.com/akohli96/PlayThatSong
cd PlayThatSong
virtualenv .env
source .env/bin/activate
pip install -r requirements.txt
###Place Youtube Data API keys in the cred.py file

python server.py

```
Go sing a song at 127.0.0.1:5000 :smile:
