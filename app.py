from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import instaloader
from pytube import YouTube

app = Flask(__name__)
CORS(app)

# Function to get Instagram video details
def get_instagram_video(url):
    L = instaloader.Instaloader()
    try:
        shortcode = url.split("/")[-2]
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        if post.is_video:
            return {
                'title': post.title or "Instagram Video",
                'thumbnail': post.url,
                'download_url': post.video_url
            }
        else:
            return None
    except Exception as e:
        return None

# Function to get YouTube video details
def get_youtube_video(url):
    try:
        yt = YouTube(url)
        return {
            'title': yt.title,
            'thumbnail': yt.thumbnail_url,
            'download_url': yt.streams.get_highest_resolution().url
        }
    except Exception as e:
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    data = request.json
    url = data.get('url')
    platform = data.get('platform')

    if not url or not platform:
        return jsonify({'error': 'URL and platform are required'}), 400

    if platform == 'youtube':
        video_info = get_youtube_video(url)
    elif platform == 'instagram':
        video_info = get_instagram_video(url)
    else:
        return jsonify({'error': 'Invalid platform'}), 400

    if video_info:
        return jsonify(video_info)
    else:
        return jsonify({'error': 'Invalid URL or not a video'}), 500

if __name__ == '__main__':
    app.run(debug=True)
