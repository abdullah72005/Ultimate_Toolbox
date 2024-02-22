from flask import send_file
from pytube import YouTube
from werkzeug.utils import secure_filename
from helpers.functions import deleteFiles

def print_audio_streams(yt):
    # Get audio streams for a YouTube video
    yt = YouTube(yt)

    # Sort the stream from the largest file to the smallest
    streams = sorted(yt.streams.filter(only_audio=True), key=lambda s: s.filesize, reverse=True)
    return streams


def download_audio(yt, i, title):
    # Download audio and return the file path
    yt = YouTube(yt)
    selected_stream = sorted(yt.streams.filter(only_audio=True), key=lambda s: s.filesize, reverse=True)
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
    yt = YouTube(youtube_url)
    title = yt.title
    thumbnail_url = yt.thumbnail_url
    duration = yt.length
    return title, thumbnail_url, duration
    



