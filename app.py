from flask import Flask, request, send_file, jsonify
import subprocess
import os

app = Flask(__name__)

# Helper function to run subprocess commands and check for errors
def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        return result.stderr
    return result.stdout

# Ensure the output directory exists
def ensure_output_dir():
    if not os.path.exists('outputs'):
        os.makedirs('outputs')

@app.route('/translate', methods=['POST'])
def translate_and_speak():
    data = request.json
    text = data.get('text')
    target_language = data.get('target_language')
    target_mymemory_language = data.get('target_mymemory_language')
    tts_language = data.get('tts_language')
    tts_gender = data.get('tts_gender')
    tts_rate = data.get('tts_rate')
    tts_volume = data.get('tts_volume')
    tts_pitch = data.get('tts_pitch')
    api_key = data.get('api_key')

    # Validate input
    if not text or not target_language:
        return jsonify({"error": "Text and target language are required"}), 400

    # Define file paths
    input_file = 'input.txt'
    output_file = 'outputs/output.txt'
    audio_file = 'outputs/output_audio.wav'

    # Save input text to file
    with open(input_file, 'w') as f:
        f.write(text)

    ensure_output_dir()

    # Attempt translation using google.py first
    command = f"python google.py {input_file} {output_file} {target_language}"
    stderr = run_command(command)
    if "Translation complete" in stderr:
        print("Translation complete by google.py")
    else:
        # If google.py fails, try mymemory.py
        command = f"python mymemory.py {input_file} {output_file} {target_mymemory_language}"
        stderr = run_command(command)
        if "Translation complete" in stderr:
            print("Translation complete by mymemory.py")
        else:
            # If both google.py and mymemory.py fail, try chatgpt.py
            if not api_key:
                return jsonify({"error": "API key is required for chatgpt.py"}), 400

            command = f"python chatgpt.py {input_file} {output_file} {api_key} {target_language}"
            stderr = run_command(command)
            if "Translation complete" in stderr:
                print("Translation complete by chatgpt.py")
            else:
                os.remove(input_file)
                return jsonify({"error": "Translation failed"}), 500

    # Text-to-Speech using tts.py
    command = f"python tts.py --input {output_file} --output {audio_file} --language={tts_language} --gender={tts_gender} --rate={tts_rate} --volume={tts_volume} --pitch={tts_pitch}"
    stderr = run_command(command)
    if "Selected voice" in stderr:
        print("TTS complete")
    else:
        os.remove(input_file)
        os.remove(output_file)
        return jsonify({"error": "TTS failed"}), 500

    # Stream the output audio file
    if os.path.exists(audio_file):
        os.remove(input_file)
        os.remove(output_file)
        return send_file(audio_file, mimetype='audio/wav')
    else:
        os.remove(input_file)
        os.remove(output_file)
        return jsonify({"error": "Audio file not found"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
