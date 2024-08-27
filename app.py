from flask import Flask, request, jsonify
from gtts import gTTS
import os

app = Flask(__name__)

@app.route('/text-to-speech', methods=['POST'])
def text_to_speech():
    data = request.get_json()
    text = data.get('text', '')
    if text:
        tts = gTTS(text=text, lang='en')
        file_path = '/app/audio.mp3'
        tts.save(file_path)
        return jsonify({'message': 'Audio file created successfully', 'audio_url': f'/audio.mp3'})
    return jsonify({'error': 'No text provided'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0')   # Asegúrate de usar host='0.0.0.0' y port=5000
