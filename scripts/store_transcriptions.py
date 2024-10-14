from utils.config_utils import load_config
from utils.transcription_utils import generate_categorization
import os
import json

def update_transcription(video_title):
    config = load_config()
    pre_processed_path = config["paths"]["preprocessed_videos"]

    # Search if the video title exists in the preprocessed folder
    video_files = [f for f in os.listdir(pre_processed_path) if f.endswith(".json")]
    print(f"Video files: {video_files}")
    matching_files = [f for f in video_files if video_title in f]

    if matching_files:
        print(f"Updating {len(matching_files)} transcriptions")

        # Read the transcription from the file
        with open(os.path.join(pre_processed_path, f"{video_title}.json"), "r") as f:
            transcription = json.load(f)

        # Extract hook, buildup, and CTA from the 'body' field
        body_text = transcription["body"]
        hook, buildup, cta = generate_categorization(body_text)

        # Update the transcription with new fields
        updated_transcription = {
            "date": transcription["date"],
            "Reference URL": transcription["Reference URL"],
        }

        # Store the extracted sections in the original transcription and remove them from the 'body' field
        if hook:
            updated_transcription["Hook"] = hook
            body_text = body_text.replace(hook, "")
        if buildup:
            updated_transcription["Build Up"] = buildup
            body_text = body_text.replace(buildup, "")
        if cta:
            updated_transcription["CTA"] = cta
            body_text = body_text.replace(cta, "")

        # Update the 'body' field with the remaining text
        updated_transcription["body"] = body_text.strip()

        # Write the updated transcription back to the file
        with open(os.path.join(pre_processed_path, f"{video_title}.json"), "w") as f:
            json.dump(updated_transcription, f, indent=4)

        print(f"Updated transcription for {video_title}")


if __name__ == "__main__":
    update_transcription("Videobyonlyzita")
