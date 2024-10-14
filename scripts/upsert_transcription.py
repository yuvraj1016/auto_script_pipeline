from utils.storage_utils import store_in_google_sheets
from utils.config_utils import load_config
import os
import json

def upsert(video_title):
    config = load_config()
    pre_processed_path = config["paths"]["preprocessed_videos"]

    transcriptions = []

    # Find the video title in the processed folder
    video_files = [f for f in os.listdir(pre_processed_path) if f.endswith(".json")]
    print(f"Video files: {video_files}")

    matching_files = [f for f in video_files if video_title in f]
    if matching_files:
        print(f"Updating {len(matching_files)} transcriptions")

        # Read the transcription from the file
        with open(os.path.join(pre_processed_path, f"{video_title}.json"), "r") as f:
            data = json.load(f)
            transcription = [
                data.get("date", ""),
                data.get("Reference URL", ""),
                data.get("Hook", ""),
                data.get("Build Up", ""),
                data.get("body", ""),
                data.get("CTA", "")
            ]
            transcriptions.append(transcription)

        store_in_google_sheets(transcriptions)
