from flask import Flask, request, jsonify, send_from_directory
from gtts import gTTS
import os

app = Flask(__name__)

# Usar el directorio temporal de Render para almacenar el archivo de audio
AUDIO_DIR = '/tmp'
AUDIO_FILE = 'audio.mp3'

# Almacena el texto más reciente para propósitos de demostración
latest_command = 'Hola mundo'  # Puedes actualizar esto desde otro lugar según sea necesario

@app.route('/text-to-speech', methods=['POST'])
def text_to_speech():
    data = request.get_json()
    text = data.get('text', '')
    if text:
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
    # Devuelve el texto más reciente o el comando
    return jsonify({'text': latest_command})

if __name__ == '__main__':
    app.run(host='0.0.0.0')
