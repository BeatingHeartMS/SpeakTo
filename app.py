from flask import Flask, request, jsonify, send_from_directory
from gtts import gTTS
import os

app = Flask(__name__)

# Usar el directorio temporal de Render para almacenar el archivo de audio
AUDIO_DIR = '/tmp'
AUDIO_FILE = 'audio.mp3'

# Variable global para almacenar el último texto procesado
last_processed_text = ""

@app.route('/text-to-speech', methods=['POST'])
def text_to_speech():
    global last_processed_text
    data = request.get_json()
    text = data.get('text', '')
    if text:
        if text != last_processed_text:  # Procesa solo si el texto es diferente
            last_processed_text = text
            tts = gTTS(text=text, lang='es')  # Usa el idioma deseado aquí
            file_path = os.path.join(AUDIO_DIR, AUDIO_FILE)
            tts.save(file_path)
        return jsonify({'message': 'Audio file created successfully', 'audio_url': f'/audio.mp3'})
    return jsonify({'error': 'No text provided'}), 400

@app.route('/audio.mp3')
def serve_audio():
    return send_from_directory(AUDIO_DIR, AUDIO_FILE)

@app.route('/get-latest-command', methods=['GET'])
def get_latest_command():
    global last_processed_text
    return jsonify({'text': last_processed_text})

if __name__ == '__main__':
    app.run(host='0.0.0.0')

