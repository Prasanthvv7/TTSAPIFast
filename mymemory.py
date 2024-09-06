from deep_translator import MyMemoryTranslator
import argparse

# Function to split text into chunks of less than 500 characters
def split_text_into_chunks(text, max_length=400):
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

def translate_file(input_file_path, output_path, target_language):
    # Initialize the MyMemoryTranslator with source language as English and target language
    translator = MyMemoryTranslator(source='english', target=target_language)

    try:
        # Read the content of the input file
        with open(input_file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        # Split the text into chunks if it's larger than 500 characters
        text_chunks = split_text_into_chunks(text)

        # Perform translation on each chunk
        translated_text = ""
        for chunk in text_chunks:
            translated_chunk = translator.translate(chunk)
            translated_text += translated_chunk

        # Write the translated content to the output file
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(translated_text)

        print(f'Translation complete. Translated text saved to {output_path}')

    except Exception as e:
        print(f'An error occurred: {e}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Translate text from a file to a target language using MyMemory.")
    parser.add_argument("input_file", help="Path to the input text file.")
    parser.add_argument("output_file", help="Path to the output text file.")
    parser.add_argument("target_language", help="Target language for translation (e.g., 'de', 'fr', 'es').")

    args = parser.parse_args()

    translate_file(args.input_file, args.output_file, args.target_language)
