from flask import Flask, request, jsonify, send_from_directory
from gtts import gTTS
import os

app = Flask(__name__)

AUDIO_DIR = '/tmp'

@app.route('/text-to-speech', methods=['POST'])
def text_to_speech():
    data = request.get_json()
    text = data.get('text', '')
    if text:
        tts = gTTS(text=text, lang='es', tld='com.ar')
        file_path = os.path.join(AUDIO_DIR, 'audio.mp3')
        tts.save(file_path)
        # Asegúrate de devolver la URL completa y válida
        return jsonify({'message': 'Audio file created successfully', 'audio_url': f'https://speakto.onrender.com/audio.mp3'})
    return jsonify({'error': 'No text provided'}), 400

@app.route('/audio.mp3')
def get_audio():
    # Asegúrate de que la ruta del archivo sea correcta
    return send_from_directory(AUDIO_DIR, 'audio.mp3')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
