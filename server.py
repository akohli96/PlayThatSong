import os, json
from flask import Flask
from watson_developer_cloud import AuthorizationV1 as Authorization
from watson_developer_cloud import SpeechToTextV1 as SpeechToText

# Speech to Text
STT_USERNAME = None # '<Speech to Text username>'
STT_PASSWORD = None # '<Speech to Text password>'

app = Flask(__name__, static_url_path='')

@app.route('/')
def root():
  return app.send_static_file('microphone-streaming.html')

@app.route('/api/speech-to-text/token')
def getSttToken():
	print(STT_USERNAME)
	authorization = Authorization(username=STT_USERNAME, password=STT_PASSWORD)
	return authorization.get_token(url=SpeechToText.default_url)

app.run(debug=True)
