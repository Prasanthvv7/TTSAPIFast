# TTSAPIFast

Translation and Text-to-Speech API
This Flask API translates text using multiple services and then converts the translated text to speech. It follows this sequence:

Translation Services:

mymemory.py: First attempt for translation.
google.py: Second attempt if mymemory.py fails.
chatgpt.py: Final attempt if both previous services fail (requires an API key).
Text-to-Speech:

tts.py: Converts the final translated text to speech.
Prerequisites
Python (3.x recommended)
bash setup.sh
API Endpoint
POST /translate
This endpoint translates the provided text and converts it to speech.

Request
Send a POST request to http://localhost:5000/translate with the following JSON payload:

json
Copy code
{
    "text": "Everyone has the right to education. Education shall be free, at least in the elementary and fundamental stages.",
    "target_language": "tamil",
    "target_mymemory_language": "tamil india",
    "tts_language": "ta",
    "tts_gender": "female",
    "tts_rate": "+0%",
    "tts_volume": "+0%",
    "tts_pitch": "+0Hz",
    "api_key": "OPEN_AI_API_KEY"
}
curl Example
You can use curl to test the API:

bash
Copy code
curl --location 'http://localhost:5000/translate' \
--header 'Content-Type: application/json' \
--data '{
    "text": "Everyone has the right to education. Education shall be free, at least in the elementary and fundamental stages.",
    "target_language": "tamil",
    "target_mymemory_language": "tamil india",
    "tts_language": "ta",
    "tts_gender": "female",
    "tts_rate": "+0%",
    "tts_volume": "+0%",
    "tts_pitch": "+0Hz",
    "api_key": "OPENAI_API_KEY"
}'
Response
Success: The API will return the output_audio.wav file as an audio stream if the process completes successfully.
Error: If the process fails at any stage, a JSON response with an error message will be returned.
Running the API
Navigate to the directory containing app.py and the scripts.
Start the Flask server:
bash
Copy code
python app.py
The API will be available at http://localhost:5000.
Notes
Ensure that the mymemory.py, google.py, chatgpt.py, and tts.py scripts are executable and properly configured.
The input.txt file should contain the text you want to translate, and the outputs directory will contain the output.txt and output_audio.wav files.
Troubleshooting
Check the console logs for error messages if the API does not work as expected.
Verify that all scripts and dependencies are installed and correctly configured.
