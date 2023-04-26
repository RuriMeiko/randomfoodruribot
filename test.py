import requests

from translate import Translator

with open('output.ogg','rb') as audio:
    payload = {
        'chat_id': -845506997,
        'caption': 'alo'
    }
    files = {
        'voice': audio.read(),
    }
    resp = requests.post(
        "https://api.telegram.org/bot{token}/sendVoice".format(token='5736528142:AAEFBtsWq37N4ADtrsTTssAOG8BOn4PK4PU'),
        data=payload,
        files=files).json()

# from pydub import AudioSegment

# # # set input and output file paths
# input_file = "temp\\user_voice.wav"
# output_file = "output.ogg"

# # load audio file with pydub
# audio = AudioSegment.from_wav(input_file)

# # export audio file with opus encoding using pydub
# audio.export(output_file, format='ogg', codec='libopus')


