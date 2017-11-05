import os, json
from flask import Flask, render_template, jsonify,request
from watson_developer_cloud import AuthorizationV1 as Authorization
from watson_developer_cloud import SpeechToTextV1 as SpeechToText
from cred import speech_auth
from py_genius import Genius
from apiclient.discovery import build

STT_USERNAME = speech_auth['username']
STT_PASSWORD = speech_auth['password']
GENIUS_TOKEN = speech_auth['auth']
YOUTUBE_DEVELOPER_KEY = speech_auth['youtube_key']
YOUTUBE_API_SERVICE_NAME = speech_auth['youtube_service']
YOUTUBE_API_VERSION = speech_auth['yotube_version']

app = Flask(__name__, static_url_path='')
api = Genius(GENIUS_TOKEN)
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=YOUTUBE_DEVELOPER_KEY)

@app.route('/')
def root():
  return app.send_static_file('microphone-streaming-text-to-console.html')

@app.route('/api/speech-to-text/token')
def get_speech_token():
  #print(STT_USERNAME)
  authorization = Authorization(username=STT_USERNAME, password=STT_PASSWORD)
  return authorization.get_token(url=SpeechToText.default_url)

@app.route('/api/search',methods=['POST'])
def get_quote():
  #print request.json['search']
  search=request.json['search']
  #print search
  result = api.search(search)
  top_results={}
  for i,sub_result in enumerate(result['response']['hits'][:3]):
    subset=sub_result['result']
    top_results[i]={'title': subset['title'],'artist':subset['primary_artist']['name'] }
  print top_results
  return jsonify(top_results)

@app.route('/api/video',methods=['POST'])
def get_video_url():
    print("REQUESTED")
    search_response = youtube.search().list(
        q=request.json['search'],
        part='id',
        maxResults=2
    ).execute()
    print(search_response)
    videos={}

    for i,search_result in enumerate(search_response.get('items', [])):
        videos[i]="https://www.youtube.com/watch?v="+str(search_result['id']['videoId'])

    return jsonify(videos)

app.run(debug=True)
