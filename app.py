
from flask import Flask, request, render_template, jsonify
from pytube import YouTube
import os
import threading

app = Flask(__name__)

# Set the download folder
DOWNLOAD_FOLDER = 'downloads'
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

# Create the download folder if it doesn't exist
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

def download_video(video_url):
    try:
        # Create a YouTube object
        yt = YouTube(video_url)

        # Get the highest resolution stream
        video_stream = yt.streams.get_highest_resolution()

        # Generate a unique filename for the download
        filename = f"{yt.title}.mp4"
        filepath = os.path.join(app.config['DOWNLOAD_FOLDER'], filename)

        # Download the video
        video_stream.download(output_path=app.config['DOWNLOAD_FOLDER'])

        return {"status": "success", "message": "Download complete!", "filename": filename}

    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video_route():
    try:
        # Get the video URL from the form data
        video_url = request.form['video_url']

        # Start the download in a separate thread to avoid blocking the main thread
        download_thread = threading.Thread(target=download_video, args=(video_url,))
        download_thread.start()

        response = {"status": "success", "message": "Download started in the background."}
        return jsonify(response)

    except Exception as e:
        response = {"status": "error", "message": str(e)}
        return jsonify(response), 500

if __name__ == '__main__':
    app.run(debug=True)


















# from flask import Flask, request, render_template, jsonify
# from pytube import YouTube

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/download', methods=['POST'])
# def download_video():
#     try:
#         # Get the video URL from the form data
#         video_url = request.form['video_url']

#         # Create a YouTube object
#         yt = YouTube(video_url)

#         # Get the highest resolution stream
#         video_stream = yt.streams.get_highest_resolution()

#         # Download the video
#         video_stream.download()

#         response = {"status": "success", "message": "Download complete!"}
#         return jsonify(response)

#     except Exception as e:
#         response = {"status": "error", "message": str(e)}
#         return jsonify(response), 500

# if __name__ == '__main__':
#     app.run(debug=True)




