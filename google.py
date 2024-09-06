from deep_translator import GoogleTranslator
import argparse

# Function to split text into chunks of less than 4700 characters
def split_text_into_chunks(text, max_length=4700):
    chunks = []
    while len(text) > max_length:
        # Find the nearest space or punctuation mark to avoid cutting words in half
        split_index = text.rfind(' ', 0, max_length)
        if split_index == -1:
            split_index = max_length  # If no space is found, split at max_length
        chunks.append(text[:split_index].strip())  # Remove trailing spaces
        text = text[split_index:].lstrip()  # Remove leading spaces
    chunks.append(text.strip())  # Append the remaining text as the last chunk
    return chunks

def translate_file(input_file_path, output_file_path, target_google_language):
    # Initialize the translator
    translator = GoogleTranslator(target=target_google_language, source='english')

    try:
        # Read the content of the input file
        with open(input_file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        # Split the text into chunks if it's larger than 4700 characters
        text_chunks = split_text_into_chunks(text)

        # Perform translation on each chunk
        translated_text = ""
        for chunk in text_chunks:
            translated_text += translator.translate(chunk)

        # Write the translated text to the output file
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(translated_text)

        print(f"Translation complete. Translated text by Google written to {output_file_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Translate text from a file to a target language using Google Translator.")
    parser.add_argument("input_file", help="Path to the input text file.")
    parser.add_argument("output_file", help="Path to the output text file.")
    parser.add_argument("target_google_language", help="Target language for translation (e.g., 'de', 'fr', 'es').")

    args = parser.parse_args()

    translate_file(args.input_file, args.output_file, args.target_google_language)
