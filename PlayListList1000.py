# from googleapiclient import discovery
from googleapiclient.discovery import build
from urllib.parse import parse_qs, urlparse
from pytube import YouTube
import sys, traceback
import os, ssl
import csv

def download_youtube(url, output):
    """Download YouTube videos.

    Args:
        url (str): YouTube video url.
        output (str): Download directory.

    Returns:
        bool: Return True if the video was downloaded and False if get an exception.

    """
    # try:
    YouTube(url).streams.first().download(output)
    # return True
    # except (ValueError, Exception):
    #     return False


if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
        getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context
# extract playlist id from url
PlayListUrl = 'https://www.youtube.com/playlist?list=PLsY5cGNN2qQM1h9rBMhF3NspOAhs8co34'
query = parse_qs(urlparse(PlayListUrl).query, keep_blank_values=True)
playlist_id = query ["list"] [0]

print(f'get all playlist items links from {playlist_id}')
youtube = build("youtube", "v3", developerKey="")

request = youtube.playlistItems().list(
    part="snippet",
    playlistId=playlist_id,
    maxResults=50
)
response = request.execute()

playlist_items = []
while request is not None:
    response = request.execute()
    playlist_items += response ["items"]
    request = youtube.playlistItems().list_next(request, response)

print(f"total: {len(playlist_items)}")

# print([
#     f'https://www.youtube.com/watch?v={t ["snippet"] ["resourceId"] ["videoId"]}&list={playlist_id}&t=0s'
#     for t in playlist_items
# ])
successes = 0
with open('video_files.csv', mode='w') as video_file:
    fieldnames = ['URL', 'FileName', 'description', 'Title']
    video_writer = csv.writer(video_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)


for t in playlist_items:
    Vidoe = {"Url" : 2, "Description" : 1, "Title" : 3}
    Video.update ({'Url': f'https://www.youtube.com/watch?v={t ["snippet"] ["resourceId"] ["videoId"]}&list={playlist_id}&t=0s'})
    Video.update  = ('Description': t ["snippet"]["description"])
    Video.update  = ('Title': t ["snippet"]["title"])
    try:
        # Retry
        print("Downloading ", Video {'Url'})
        if download_youtube(Video {'Url'}, "."):
            video_writer.writerow(['John Smith', 'Accounting', 'November'])
            video_writer.writerow(['Erica Meyers', 'IT', 'March'])
            successes += 1

            continue

    except (ValueError, Exception):
        print("{} failed for".format(VideoUrl))
        print("Exception in user code:")
        print("-" * 60)
        traceback.print_exc(file=sys.stdout)
        print("-" * 60)

print("Playlist complete")
