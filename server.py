import os, json
from flask import Flask
from watson_developer_cloud import AuthorizationV1 as Authorization
from watson_developer_cloud import SpeechToTextV1 as SpeechToText
from cred import speech_auth

# Speech to Text
STT_USERNAME = speech_auth['username'] 
STT_PASSWORD = speech_auth['password'] 

app = Flask(__name__, static_url_path='')

@app.route('/')
def root():
  return app.send_static_file('microphone-streaming-text-to-console.html')

@app.route('/api/speech-to-text/token')
def getSttToken():
	print(STT_USERNAME)
	authorization = Authorization(username=STT_USERNAME, password=STT_PASSWORD)
	return authorization.get_token(url=SpeechToText.default_url)

app.run(debug=True)
