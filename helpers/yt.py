from flask import send_file
from pytubefix import YouTube, Playlist
from werkzeug.utils import secure_filename
from helpers.functions import deleteFiles
from urllib.parse import urlparse

# def isPlaylist(youtube_url):
#     try:
#         Playlist(youtube_url)
#         return True
#     except:
#         return False

def print_audio_streams(youtube_url, fileType):
    # Get audio streams for a YouTube video
    youtube_url = YouTube(youtube_url)

    # Sort the stream from the largest file to the smallest and check the file type
    if fileType == "Audio":
        streams = sorted(youtube_url.streams.filter(only_audio=True), key=lambda s: s.filesize, reverse=True)
    elif fileType == 'Video':
        streams = sorted((stream for stream in youtube_url.streams if stream.audio_codec is not None and stream.video_codec is not None), key=lambda s: s.filesize, reverse=True)
    return streams


def download_audio(youtube_url, i, title, fileType):
    # Download audio and return the file path
    youtube_url = YouTube(youtube_url)
    # check the file type  
    if fileType == 'Audio':
        ext = ".mp3"
        selected_stream = sorted(youtube_url.streams.filter(only_audio=True), key=lambda s: s.filesize, reverse=True)
        ss = selected_stream[i]
    elif fileType == 'Video':
        ext = ".mp4"
        selected_stream = sorted(youtube_url.streams.filter(file_extension='mp4'), key=lambda s: s.filesize, reverse=True)
        ss = selected_stream[i]

    # Download the file to the specified path
    out_file = ss.download(output_path="static/uploads", filename=f"{secure_filename(title)}{ext}")

    # Send the downloaded file as an attachment
    outputfile = send_file(out_file, as_attachment=True, download_name=f"{title}{ext}")

    # Delete the files in the directory
    deleteFiles("static/uploads")

    #return the file
    return outputfile

def get_video_info(youtube_url):
    # Get title, thumbnail, and duration of a YouTube video
    youtube_url = YouTube(youtube_url)
    title = youtube_url.title
    author = youtube_url.author
    views = youtube_url.views
    rating = youtube_url.rating
    duration = youtube_url.length
    publishDate = youtube_url.publish_date
    thumbnail_url = youtube_url.thumbnail_url
    return title, author, views, rating, duration, publishDate, thumbnail_url
    
# check if link is in valid format
def isValidURL(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False



