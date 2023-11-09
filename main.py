from concurrent.futures import ThreadPoolExecutor, as_completed
import os
from gtts import gTTS
import pygame
from time import sleep


# Function to split the text into paragraphs
def split_in_paragraphs(text):
    return [para.strip() for para in text.split('\n\n') if para.strip()]


# Function to save a paragraph as speech to a file
def save_speech_to_file(part_text, part_number, language='en', cache_dir='tts_cache'):
    part_mp3_file = os.path.join(cache_dir, f"output_paragraph_{part_number}.mp3")
    tts = gTTS(text=part_text, lang=language, slow=False)
    tts.save(part_mp3_file)
    return part_mp3_file


# Define the path to the text file you want to read
text_file_path = 'the_text.txt'

# Read the text from the file
with open(text_file_path, 'r', encoding='utf-8') as file:
    mytext = file.read()

# Language in which you want to convert
language = 'en'

# Splitting the text into paragraphs
paragraphs = split_in_paragraphs(mytext)

# Define a directory to store cached audio files
cache_dir = 'tts_cache'
os.makedirs(cache_dir, exist_ok=True)


# Process paragraphs using ThreadPoolExecutor
def generate_audio_files(paragraphs, language):
    with ThreadPoolExecutor() as executor:
        # Create a future to part number mapping
        future_to_part = {executor.submit(save_speech_to_file, para, idx, language, cache_dir): idx for idx, para in
                          enumerate(paragraphs)}
        # As each future completes, print out a confirmation message
        for future in as_completed(future_to_part):
            part_number = future_to_part[future]
            try:
                # Wait for the audio file to be saved and get the filename
                part_mp3_file = future.result()
                print(f"Paragraph {part_number + 1} audio saved as {part_mp3_file}")
            except Exception as exc:
                print(f"Paragraph {part_number + 1} generated an exception: {exc}")


# Call the function to generate audio files
generate_audio_files(paragraphs, language)

# Initialize the mixer module
pygame.mixer.init()


# Function to play the generated audio files
def play_audio_files(paragraphs, cache_dir='tts_cache'):
    for part_number, part_text in enumerate(paragraphs):
        part_mp3_file = os.path.join(cache_dir, f"output_paragraph_{part_number}.mp3")
        if os.path.exists(part_mp3_file):
            # Print the part number and the text being read to the terminal
            print(f"Reading paragraph {part_number + 1}/{len(paragraphs)}...\n")
            print(part_text)  # Print the text of the current paragraph

            # Load the audio file and play it
            pygame.mixer.music.load(part_mp3_file)
            pygame.mixer.music.play()

            # Wait for playback to finish for this paragraph
            while pygame.mixer.music.get_busy():
                sleep(1)


# Call the function to play audio files
play_audio_files(paragraphs, cache_dir)

# Remember to quit pygame when done
pygame.quit()
