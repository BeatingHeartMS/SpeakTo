from flask import Flask, request, jsonify, send_from_directory
from gtts import gTTS
import os

app = Flask(__name__)

# Usar el directorio temporal de Render para almacenar el archivo de audio
AUDIO_DIR = '/tmp'

@app.route('/text-to-speech', methods=['POST'])
def text_to_speech():
    data = request.get_json()
    text = data.get('text', '')
    if text:
        tts = gTTS(text=text, lang='es', tld='com.ar')
        file_path = os.path.join(AUDIO_DIR, 'audio.mp3')
        tts.save(file_path)
        return jsonify({'message': 'Audio file created successfully', 'audio_url': '/audio.mp3'})
    return jsonify({'error': 'No text provided'}), 400


@app.route('/audio.mp3', methods=['GET'])
def get_audio():
    # Servir el archivo de audio desde el directorio temporal
    return send_from_directory(AUDIO_DIR, 'audio.mp3')

if __name__ == '__main__':
    app.run(host='0.0.0.0')

