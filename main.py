from flask import Flask, request, jsonify, send_file
from pytube import YouTube
import os
import re

app = Flask(__name__)

def download_video(url, resolution):
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4', resolution=resolution).first()
        if stream:
            # Define the download path
            download_path = stream.download(output_path='/cache', filename='video.mp4')  # Change this path
            return download_path, None  # Return the path of the downloaded video
        else:
            return None, "Video with the specified resolution not found."
    except Exception as e:
        return None, str(e)

def is_valid_youtube_url(url):
    pattern = r"^(https?://)?(www\.)?youtube\.com/watch\?v=[\w-]+(&\S*)?$"
    return re.match(pattern, url) is not None

@app.route('/download', methods=['POST'])
def download_by_url_and_resolution():
    data = request.get_json()
    url = data.get('url')
    resolution = data.get('resolution')

    if not url or not resolution:
        return jsonify({"error": "Missing 'url' or 'resolution' parameter in the request body."}), 400

    if not is_valid_youtube_url(url):
        return jsonify({"error": "Invalid YouTube URL."}), 400
    
    download_path, error_message = download_video(url, resolution)
    
    if download_path:
        return send_file(download_path, as_attachment=True), 200  # Send the video file as an attachment
    else:
        return jsonify({"error": error_message}), 500

if __name__ == '__main__':
    app.run(debug=True)
