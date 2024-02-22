from flask import send_file
from pytube import YouTube
from werkzeug.utils import secure_filename
from helpers.functions import deleteFiles

def print_audio_streams(youtube_url):
    # Get audio streams for a YouTube video
    youtube_url = YouTube(youtube_url)

    # Sort the stream from the largest file to the smallest
    streams = sorted(youtube_url.streams.filter(only_audio=True), key=lambda s: s.filesize, reverse=True)
    return streams


def download_audio(youtube_url, i, title):
    # Download audio and return the file path
    youtube_url = YouTube(youtube_url)
    selected_stream = sorted(youtube_url.streams.filter(only_audio=True), key=lambda s: s.filesize, reverse=True)
    ss = selected_stream[i]
    
    # Download the audio file to the specified path
    out_file = ss.download(output_path="static/uploads", filename=f"{secure_filename(title) + '.mp3'}")

    # Send the downloaded file as an attachment
    outputfile = send_file(out_file, as_attachment=True, download_name=f"{title}.mp3")

    # Delete the files in the directory
    deleteFiles("static/uploads")

    return outputfile

def get_video_info(youtube_url):
    # Get title, thumbnail, and duration of a YouTube video
    youtube_url = YouTube(youtube_url)
    title = youtube_url.title
    thumbnail_url = youtube_url.thumbnail_url
    duration = youtube_url.length
    return title, thumbnail_url, duration
    



