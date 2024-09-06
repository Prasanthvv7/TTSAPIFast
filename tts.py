import argparse
import asyncio
import os
import random
import edge_tts
from edge_tts import VoicesManager

# Parse command-line arguments
parser = argparse.ArgumentParser(description="TTS synthesis with custom parameters.")
parser.add_argument('--input', type=str, required=True, help="Path to the input text file")
parser.add_argument('--output', type=str, required=True, help="Name of the output audio file")
parser.add_argument('--language', type=str, required=True, help="Language code (e.g., 'es' for Spanish)")
parser.add_argument('--gender', type=str, required=True, choices=['male', 'female'], help="Voice gender")
parser.add_argument('--rate', type=str, default="+0%", help="Speech rate")
parser.add_argument('--volume', type=str, default="+0%", help="Speech volume")
parser.add_argument('--pitch', type=str, default="+0Hz", help="Speech pitch")
args = parser.parse_args()


# Full path for the output file
output_file_path = args.output

def read_text_file(file_path):
    """Read the input text from the file."""
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except IOError as e:
        print(f"Error reading file {file_path}: {e}")
        raise

async def amain(text: str) -> None:
    """Main function"""
    voices = await VoicesManager.create()
    voice = voices.find(Gender=args.gender.capitalize(), Language=args.language)
    if not voice:
        raise ValueError(f"No voice found for language {args.language} and gender {args.gender}")

    selected_voice = random.choice(voice)["Name"]
    print(f"Selected voice: {selected_voice}")

    try:
        communicate = edge_tts.Communicate(
            text,
            selected_voice,
            rate=args.rate,
            volume=args.volume,
            pitch=args.pitch
        )
        await communicate.save(output_file_path)
    except edge_tts.exceptions.NoAudioReceived as e:
        print(f"No audio was received: {e}")
        raise
    except ValueError as e:
        print(f"Error initializing Communicate: {e}")
        raise

if __name__ == "__main__":
    text = read_text_file(args.input)
    asyncio.run(amain(text))