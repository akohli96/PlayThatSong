import os, json
from flask import Flask, render_template, jsonify,request
from watson_developer_cloud import AuthorizationV1 as Authorization
from watson_developer_cloud import SpeechToTextV1 as SpeechToText
from cred import speech_auth
from py_genius import Genius

# Speech to Text
STT_USERNAME = speech_auth['username'] 
STT_PASSWORD = speech_auth['password'] 
GENIUS_TOKEN = speech_auth['auth']

app = Flask(__name__, static_url_path='')
api = Genius(GENIUS_TOKEN)

@app.route('/')
def root():
  return app.send_static_file('microphone-streaming-text-to-console.html')

@app.route('/api/speech-to-text/token')
def getSttToken():
  #print(STT_USERNAME)
  authorization = Authorization(username=STT_USERNAME, password=STT_PASSWORD)
  return authorization.get_token(url=SpeechToText.default_url)

@app.route('/api/search',methods=['POST'])
def get_quote():
  #print request.json['search']
  search=request.json['search']
  result = api.search(search)
  for sub_result in result['response']['hits'][:3]:
    to_parse=sub_result['result']
    print to_parse['title'],to_parse['primary_artist']['name']
  return jsonify(result)


app.run(debug=True)
