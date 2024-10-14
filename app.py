from flask import Flask, request, jsonify
import concurrent.futures
from scripts.extract_videos import download_video_audio
from scripts.transcribe_videos import video_transcribe
from scripts.store_transcriptions import update_transcription
from scripts.upsert_transcription import upsert
from scripts.final_processing import fromat_transcription

app = Flask(__name__)

def process_url(url):
    # Download the video and audio
    video_title = download_video_audio(url)
    print(f"Processing video: {video_title}")
    
    # Transcribe the video
    video_transcribe(url, video_title)

    # Update the transcription
    update_transcription(video_title)

    # Upsert the transcription to Google Sheets
    upsert(video_title)

@app.route('/process', methods=['POST'])
def process_videos():
    urls = request.json.get('urls', [])
    if not urls:
        return jsonify({"error": "No URLs provided"}), 400
    
    # Use a ThreadPoolExecutor to download, transcribe and rename the videos in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(process_url, urls)
    
    # Use the final_processing.py script
    processed_files = fromat_transcription(urls)
    if len(processed_files) == len(urls):
        return jsonify({"message": "All files processed successfully", "processed_files": processed_files}), 200
    else:
        return jsonify({"message": "Some files failed to process. You can try them later", "processed_files": processed_files}), 206

if __name__ == '__main__':
    app.run(debug=True)
