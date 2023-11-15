import logging
import re
import os
from pytube import YouTube
from subsai import SubsAI
import json

# Configuration for error logging
logging.basicConfig(filename='errors.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Function to obtain links from the 'links.txt' file
def obtain_links_from_file():
    link_regex = re.compile(r'(https?://[^\s]+)')  # Regular expression to find HTTP/HTTPS links
    with open('links.txt') as file:
        content = file.read()
    return link_regex.findall(content)

# Function to remove a specific link from the 'links.txt' file
def remove_link_from_file(link):
    links_list = obtain_links_from_file()
    links_list.remove(link)
    with open('links.txt', 'w') as file:
        file.write('\n'.join(links_list))

# Function to create a directory for subtitles if it does not exist
def create_subtitles_directory(directory_name):
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)

# Function to clean illegal characters in file names
def clean_youtube_title(filename):
    illegal_chars = r'[<>:"/\\|?*]'  # Illegal characters in file names
    cleaned_video_title = re.sub(illegal_chars, '', str(filename))  # Replace illegal characters
    return cleaned_video_title

# Function to download a video from a link to a specific directory
def download_video(link, output_directory):
    video = YouTube(link)
    highest_resolution_stream = video.streams.get_highest_resolution()
    download_path = highest_resolution_stream.download(output_path=output_directory)
    return download_path

# Function to transcribe subtitles and save them in JSON format
def transcribe_and_save_subtitles(video_path, subs_ai, output_directory):
    base_filename = os.path.splitext(os.path.basename(video_path))[0]
    cleaned_video_title = clean_youtube_title(base_filename)
    model = subs_ai.create_model('openai/whisper', {'model_type': 'base'})
    subs = subs_ai.transcribe(video_path, model)
    subtitles_file_path = os.path.join(output_directory, f'{cleaned_video_title}.json')
    subs.save(subtitles_file_path)

# Function that processes each link obtained
def process_video(link):
    subs_ai = SubsAI()
    subtitles_dir = 'subtitulos'  # Directory for subtitles
    create_subtitles_directory(subtitles_dir)  # Create directory if it does not exist
    
    try:
        download_path = download_video(link, subtitles_dir)  # Download video
        transcribe_and_save_subtitles(download_path, subs_ai, subtitles_dir)  # Transcribe subtitles
        os.remove(download_path)  # Remove downloaded video
        remove_link_from_file(link)  # Remove link from file
    except Exception as e:
        logging.error(f"Error processing link {link}: {e}")  # Error logging

# Function to merge all JSON files into a single file
def merge_json_files(directory):
    merged_data = {}  # Dictionary to store combined information

    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                data = json.load(file)  # Load data from JSON file
                merged_data[filename[:-5]] = data  # Use filename as key in combined dictionary

    # Save combined information to a new JSON file
    with open('merged_subtitles.json', 'w') as output_file:
        json.dump(merged_data, output_file, indent=4)

# Main function of the program
def main():
    links_list = obtain_links_from_file()

    for link in links_list:
        process_video(link)  # Process each link
    
    merge_json_files('subtitulos')  # Combine JSON files after processing

if __name__ == "__main__":
    main()  # Execute main function if the script is the main program
