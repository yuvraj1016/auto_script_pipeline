import torch
from transformers import pipeline
from transformers.pipelines.audio_utils import ffmpeg_read
from utils.config_utils import load_config
import os
import time

config = load_config()
raw_videos_path = config["paths"]["raw_videos"]
pre_processed_path = config["paths"]["preprocessed_videos"]
MODEL_NAME = config["transcription"]["model_name"]
FILE_LIMIT_MB = config["transcription"]["file_limit_mb"]
BATCH_SIZE = config["transcription"]["batch_size"]


device = 0 if torch.cuda.is_available() else "cpu"

pipe = pipeline(
    task="automatic-speech-recognition",
    model=MODEL_NAME,
    chunk_length_s=30,
    device=device,
)

def video_transcribe(url , video_file):
    video_files = [f for f in os.listdir(raw_videos_path) if f.endswith(".mp4")]
    print(f"Video files: {video_files}")
    matching_files = [f for f in video_files if video_file in f]
    print(f"Matching files: {matching_files}")
    if matching_files:
        print(f"Transcribing {len(matching_files)} videos")

        filepath = os.path.join(raw_videos_path, video_file)
        filepath = f"{filepath}.mp4"
        print(f"File path: {filepath}")
        file_size = os.path.getsize(filepath) / 1024 / 1024
        print(f"File size: {file_size:.2f} MB")

        if file_size > FILE_LIMIT_MB:
            print(f"File size too large: {file_size:.2f} MB")
            return

        with open(filepath, "rb") as f:
            inputs = f.read()

        print(f"Transcribing {video_file}")
        inputs = ffmpeg_read(inputs, pipe.feature_extractor.sampling_rate)
        inputs = {"array": inputs, "sampling_rate": pipe.feature_extractor.sampling_rate}

        print(f"getting params: {inputs['array'].shape}, {inputs['sampling_rate']}")
        text = pipe(inputs, batch_size=BATCH_SIZE, generate_kwargs={"task": "transcribe"}, return_timestamps=True)["text"]
        print(f"Transcription: {text}")
        # store the transcription in the pre_processed folder in the form of json with the file name as video title
        with open(os.path.join(pre_processed_path, f"{video_file}.json"), "w") as f:
            #save it in form of json with video file name and transcription
            f.write(f'{{"date" : "{time.strftime("%d/%m/%Y")}" , "Reference URL": "{url}", "body": "{text}"}}')

        print(f"Transcription saved for {video_file}")

        return text
    else:
        print(f"No matching files found for {video_file}")
        return None
    