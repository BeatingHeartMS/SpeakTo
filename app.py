from flask import Flask, request, jsonify
from gtts import gTTS
import os

app = Flask(__name__)

AUDIO_DIR = '/tmp'
last_command = None

@app.route('/text-to-speech', methods=['POST'])
def text_to_speech():
    global last_command
    data = request.get_json()
    text = data.get('text', '')
    if text:
        tts = gTTS(text=text, lang='es', tld='com.ar')
        file_path = os.path.join(AUDIO_DIR, 'audio.mp3')
        tts.save(file_path)
        last_command = text  # Almacenar el último comando
        # Cambia esta línea para devolver la URL completa del archivo de audio
        return jsonify({'message': 'Audio file created successfully', 'audio_url': f'https://speakto.onrender.com/audio.mp3'})
    return jsonify({'error': 'No text provided'}), 400

@app.route('/get-latest-command', methods=['GET'])
def get_latest_command():
    global last_command
    if last_command:
        command = last_command
        last_command = None  # Reiniciar después de enviar
        return jsonify({'text': command})
    return jsonify({'text': ''})

if __name__ == '__main__':
    app.run(host='0.0.0.0')
