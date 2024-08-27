from flask import Flask, request, jsonify
from gtts import gTTS
import os

app = Flask(__name__)

# Usar el directorio temporal de Render para almacenar el archivo de audio
AUDIO_DIR = '/tmp'
latest_command = {'text': ''}  # Inicialmente vacío

@app.route('/text-to-speech', methods=['POST'])
def text_to_speech():
    data = request.get_json()
    text = data.get('text', '')
    if text:
        tts = gTTS(text=text, lang='es')
        file_path = os.path.join(AUDIO_DIR, 'audio.mp3')
        tts.save(file_path)
        return jsonify({'message': 'Audio file created successfully', 'audio_url': '/audio.mp3'})
    return jsonify({'error': 'No text provided'}), 400

@app.route('/get-latest-command', methods=['GET'])
def get_latest_command():
    return jsonify(latest_command)

@app.route('/set-latest-command', methods=['POST'])
def set_latest_command():
    global latest_command
    data = request.get_json()
    text = data.get('text', '')
    if text:
        latest_command = {'text': text}
        return jsonify({'message': 'Command updated successfully'})
    return jsonify({'error': 'No text provided'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0')
