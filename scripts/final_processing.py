import os
import json
from utils.config_utils import load_config

def load_transcription(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def save_transcription(transcription, file_path):
    # Check if the file exists and contains a list
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                # If the file is not a valid JSON or not a list, create a new list
                data = []
    else:
        # If the file does not exist, create a new list
        data = []

    # Append the transcription to the list
    data.append(transcription)

    # Write the updated data back to the file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def fromat_transcription(urls):

    config = load_config()
    pre_processed_dir = config["paths"]["preprocessed_videos"]
    processed_dir = config["paths"]["processed_transcripts"]
    FINAL_DIR_NAME = config["paths"]["final_dir_name"]
    processed_files = []
    
    for url in urls:
        for file_name in os.listdir(pre_processed_dir):
             if file_name.endswith(".json"):
                file_path = os.path.join(pre_processed_dir, file_name)
                transcription = load_transcription(file_path)
                if transcription["Reference URL"] == url:
                    processed_files.append(file_name)
                    save_transcription(transcription, os.path.join(processed_dir, FINAL_DIR_NAME))
                    break
    return processed_files

if __name__ == "__main__":
    urls = ["https://www.instagram.com/reel/C6tMX9UAqgb/?igsh=MWV1c2dyZjczMXc4Yw==", "https://youtube.com/shorts/mZBEKEIKVLQ?si=n1MnbVS5gGGRp4ww", "https://youtu.be/Sew5tjbGgp0?si=lbQg0GoTgnRDvaA4"]
    processed_files = fromat_transcription(urls)
    print("Processed files:", processed_files)