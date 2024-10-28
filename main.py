from flask import Flask, request, jsonify, send_file
from pytube import YouTube
import os
import re
import tempfile

app = Flask(__name__)

# Route to download YouTube video
@app.route('/download', methods=['POST'])
def download_video():
    # Get the YouTube link from the request JSON
    data = request.get_json()
    youtube_url = data.get("url")

    # Check if URL is valid
    if not youtube_url or not re.match(r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})', youtube_url):
        return jsonify({"error": "Invalid YouTube URL"}), 400

    try:
        # Download the video using pytube
        yt = YouTube(youtube_url)
        video_stream = yt.streams.get_highest_resolution()

        # Save video to a temporary file
        temp_dir = tempfile.gettempdir()
        video_path = os.path.join(temp_dir, f"{yt.title}.mp4")
        video_stream.download(output_path=temp_dir, filename=f"{yt.title}.mp4")

        # Send the file as a download
        return send_file(video_path, as_attachment=True, download_name=f"{yt.title}.mp4")

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        # Clean up temporary files
        if os.path.exists(video_path):
            os.remove(video_path)

if __name__ == '__main__':
    app.run(debug=True)
