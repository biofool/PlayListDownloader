# API_KEY=AIzaSyD8kqHitMQTLrBmeGPitT1ucWcV8HWBXoE
# from googleapiclient import discovery
from googleapiclient.discovery import build
from urllib.parse import parse_qs, urlparse
from pytube import YouTube
def download_youtube(url, output):
    """Download YouTube videos.

    Args:
        url (str): YouTube video url.
        output (str): Download directory.

    Returns:
        bool: Return True if the video was downloaded and False if get an exception.

    """
    try:
        YouTube(url).streams.first().download(output)
        return True
    except (ValueError, Exception):
        return False

# extract playlist id from url
PlayListUrl = 'https://www.youtube.com/playlist?list=PLsY5cGNN2qQM1h9rBMhF3NspOAhs8co34'
query = parse_qs(urlparse(PlayListUrl).query, keep_blank_values=True)
playlist_id = query["list"][0]

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
    playlist_items += response["items"]
    request = youtube.playlistItems().list_next(request, response)

print(f"total: {len(playlist_items)}")

# print([
#     f'https://www.youtube.com/watch?v={t ["snippet"] ["resourceId"] ["videoId"]}&list={playlist_id}&t=0s'
#     for t in playlist_items
# ])
for t in playlist_items:
    # local d_video
    VideoUrl = f'https://www.youtube.com/watch?v={t ["snippet"] ["resourceId"] ["videoId"]}&list={playlist_id}&t=0s'
    try:
        # Retry
        if download_youtube(VideoUrl, "~/CABW/"):
            continue
        # object creation using YouTube
        # which was imported in the beginning
        # print("Retry status: {}".format(download_youtube(VideoUrl, "~/CABW/"),True
        # filters out all the files with "mp4" extension
        # mp4files = yt.filter('mp4')
        # d_video = yt.get(mp4files[-1].extension,mp4files[-1].resolution)
        # to set the name of the file
    except (ValueError, Exception):
        print("Download failed for:",VideoUrl)
