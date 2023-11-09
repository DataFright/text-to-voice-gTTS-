import os
import pygame
from gtts import gTTS
from time import sleep

# Initialize the mixer module
pygame.mixer.init()

# Define the path to the text file you want to read
text_file_path = 'the_text.txt'

# Read the text from the file
with open(text_file_path, 'r', encoding='utf-8') as file:
    mytext = file.read()

# Language in which you want to convert
language = 'en'

# Function to split the text into paragraphs
def split_in_paragraphs(text):
    return [para.strip() for para in text.split('\n\n') if para.strip()]

# Splitting the text into paragraphs
paragraphs = split_in_paragraphs(mytext)

# Define a directory to store cached audio files
cache_dir = 'tts_cache'
os.makedirs(cache_dir, exist_ok=True)

# Function to get a unique filename for a paragraph
def get_cache_filename(text):
    # Here we just use a simple hash, but you might want more collision-resistant approach
    return f"{hash(text)}.mp3"

# Process each paragraph
for part_number, part_text in enumerate(paragraphs):
    cache_filename = get_cache_filename(part_text)
    cache_filepath = os.path.join(cache_dir, cache_filename)

    # If we've already generated this paragraph before, use the cached file
    if not os.path.exists(cache_filepath):
        tts = gTTS(text=part_text, lang=language, slow=False)
        tts.save(cache_filepath)

    # Print the part number and the text being read to the terminal
    print(f"Reading paragraph {part_number + 1}/{len(paragraphs)}...\n")
    print(part_text)

    # Load the paragraph
    pygame.mixer.music.load(cache_filepath)

    # Play the paragraph
    pygame.mixer.music.play()

    # Wait for playback to finish for this paragraph
    while pygame.mixer.music.get_busy():
        sleep(1)
