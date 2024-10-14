import argparse
import concurrent.futures
from scripts.extract_videos import download_video_audio
from scripts.transcribe_videos import video_transcribe
from scripts.store_transcriptions import update_transcription
from scripts.upsert_transcription import upsert
from scripts.final_processing import fromat_transcription

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

def main(urls):
    # Use a ThreadPoolExecutor to download, transcribe and rename the videos in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(process_url, urls)

    # Use the final_processing.py script
    processed_files = fromat_transcription(urls)
    if len(processed_files) == len(urls):
        print("All files processed successfully")
    else:
        print("Some files failed to process. You can try them later")
        print("Processed files:", processed_files)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process video URLs.")
    parser.add_argument('urls', nargs='+', help='List of video URLs to process')
    args = parser.parse_args()
    main(args.urls)

    # Example usage:
    # python main.py https://www.instagram.com/reel/C0eV7_fCYKs/?igsh=MXRsZGszODRobnJ1MA== https://www.instagram.com/reel/C6wcq9xCAaX/
