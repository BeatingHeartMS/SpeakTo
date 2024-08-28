import os
from flask import Flask, request, jsonify, send_from_directory
from gtts import gTTS

app = Flask(__name__)

# Usar la API Key de las variables de entorno
API_KEY = os.getenv('API_KEY')

AUDIO_DIR = '/tmp'
AUDIO_FILE = 'audio.mp3'
latest_command = ''

def check_api_key(request):
    api_key = request.headers.get('X-API-KEY')
    if not api_key or api_key != API_KEY:
        return jsonify({'error': 'Unauthorized'}), 401
    return None

@app.route('/text-to-speech', methods=['POST'])
def text_to_speech():
    global latest_command
    # Verificar la API Key
    api_key_response = check_api_key(request)
    if api_key_response:
        return api_key_response  # Retorna error si la API Key no es válida
    
    data = request.get_json()
    text = data.get('text', '')
    if text:
        latest_command = text  # Actualiza el último comando
        tts = gTTS(text=text, lang='es', tld='us')  # Usa el idioma deseado aquí
        file_path = os.path.join(AUDIO_DIR, AUDIO_FILE)
        tts.save(file_path)
        return jsonify({'message': 'Audio file created successfully', 'audio_url': f'/audio.mp3'})
    return jsonify({'error': 'No text provided'}), 400

@app.route('/audio.mp3')
def serve_audio():
    # Verificar la API Key
    api_key_response = check_api_key(request)
    if api_key_response:
        return api_key_response  # Retorna error si la API Key no es válida

    # Intentar servir el archivo de audio
    try:
        return send_from_directory(AUDIO_DIR, AUDIO_FILE)
    except Exception as e:
        app.logger.error(f"Error serving audio file: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500



@app.route('/get-latest-command', methods=['GET'])
def get_latest_command():
    # Verificar la API Key
    api_key_response = check_api_key(request)
    if api_key_response:
        return api_key_response  # Retorna error si la API Key no es válida

    return jsonify({'text': latest_command})

if __name__ == '__main__':
    app.run(host='0.0.0.0')
