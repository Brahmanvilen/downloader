from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)  # Yeh zaroori hai taaki InfinityFree se request aa sake

@app.route('/download', methods=['POST'])
def get_video_info():
    data = request.json
    video_url = data.get('url')
    
    if not video_url:
        return jsonify({"error": "Link missing!"}), 400

    try:
        # yt-dlp settings
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            # Hum user ko direct video ka temporary link bhejenge
            return jsonify({
                "title": info.get('title', 'Video'),
                "download_url": info.get('url'),
                "thumbnail": info.get('thumbnail')
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
