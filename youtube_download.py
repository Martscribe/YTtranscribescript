from pytube import YouTube
import re
import logging
import requests

logging.basicConfig(filename='errors.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def obtain_links():
    link_regex = re.compile(r'(https?://[^\s]+)')
    with open('links.txt') as f:
        content = f.read()
    return link_regex.findall(content)

def remove_links(link):
    link_list.remove(link)
    with open('links.txt', 'w') as f:
        f.write('\n'.join(link_list))

def download_yt_list(link_list):
    for link in link_list:
        try:
            download_yt(link)
        except requests.HTTPError as http_err:
            logging.error(f"HTTP error occurred in {link}: {http_err}")
        except Exception as err:
            logging.exception(f"An error occurred in {link}: {err}")
        else:
            logging.info(f"Download successful for {link}")
            remove_links(link)

def download_yt(link):
    video = YouTube(link)
    youtubeObject = video.streams.get_highest_resolution()
    youtubeObject.download()


link_list = obtain_links()
download_yt_list(link_list)
