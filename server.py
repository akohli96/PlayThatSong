import os, json
from flask import Flask
from watson_developer_cloud import AuthorizationV1 as Authorization
from watson_developer_cloud import SpeechToTextV1 as SpeechToText

app = Flask(__name__, static_url_path='')

USERNAME = None
PASSWORD = None

@app.route('/')
def root():
  return app.send_static_file('index.html')

@app.route('/api/speech-to-text/tpken')
def get_token():
	authorization = Authorization(username=STT_USERNAME, password=STT_PASSWORD)
	return authorization.get_token(url=SpeechToText.default_url)

app.run(debug=True)