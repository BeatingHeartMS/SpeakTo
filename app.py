from flask import Flask, request, jsonify
from gtts import gTTS
import os

app = Flask(__name__)

# Usar el directorio temporal para almacenar el archivo de audio
AUDIO_DIR = '/tmp'
os.makedirs(AUDIO_DIR, exist_ok=True)  # Crear el directorio si no existe

@app.route('/text-to-speech', methods=['POST'])
def text_to_speech():
    data = request.get_json()
    text = data.get('text', '')
    if text:
        tts = gTTS(text=text, lang='es')  # Cambia 'en' a 'es' para español
        file_path = os.path.join(AUDIO_DIR, 'audio.mp3')
        tts.save(file_path)
        # Construir la URL completa para el archivo de audio
        audio_url = 'https://speakto.onrender.com/audio.mp3'
        return jsonify({'message': 'Audio file created successfully', 'audio_url': audio_url})
    return jsonify({'error': 'No text provided'}), 400

@app.route('/audio.mp3', methods=['GET'])
def get_audio():
    file_path = os.path.join(AUDIO_DIR, 'audio.mp3')
    if os.path.exists(file_path):
        return app.send_static_file(file_path)
    return jsonify({'error': 'Audio file not found'}), 404

@app.route('/get-latest-command', methods=['GET'])
def get_latest_command():
    # Aquí se debería implementar la lógica para obtener el último comando.
    # Este es solo un ejemplo de cómo podría devolver un texto fijo.
    return jsonify({'text': 'Hola, ¿cómo estás?'})

if __name__ == '__main__':
    app.run(host='0.0.0.0')
