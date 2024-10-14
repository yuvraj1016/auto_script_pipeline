import os
import time
import yt_dlp
from utils.config_utils import load_config
from utils.clean_title import get_clean_title
from utils.unique_id import generate_unique_id
import re

def sanitize_title(title):
    return re.sub(r'[^\w\s]', '', title)

def download_video_audio(url):
    print(f"Processing URL: {url}")
    
    info_loader = yt_dlp.YoutubeDL()
    try:
        config = load_config()
        print(f"Configuration loaded successfully: {config}")
    except Exception as e:
        print(f"Error loading configuration: {e}")
        return
    output_path = config['paths']['raw_videos']
    video_length_limit_s = config['extraction']['video_length_limit_s']
    print(f"Output path: {output_path}")
    print(f"Video length limit: {video_length_limit_s}")
    print(f"Downloading {url}")
    try:
        info = info_loader.extract_info(url, download=False)
    except yt_dlp.utils.DownloadError as err:
        print(f"Download error: {err}")
        return
    
    file_length = info["duration"]
    file_h_m_s = [int(sub_length) for sub_length in time.strftime("%H:%M:%S", time.gmtime(file_length)).split(":")]
    
    file_length_s = file_h_m_s[0] * 3600 + file_h_m_s[1] * 60 + file_h_m_s[2]
    
    if file_length_s > video_length_limit_s:
        yt_length_limit_hms = time.strftime("%H:%M:%S", time.gmtime(video_length_limit_s))
        file_length_hms = time.strftime("%H:%M:%S", time.gmtime(file_length_s))
        print(f"Maximum length is {yt_length_limit_hms}, got {file_length_hms} video.")
        return
    
    sanitize_new_title = sanitize_title(info["title"])
    unique_id = generate_unique_id(url)
    sanitize_new_title = f"{sanitize_new_title}_{unique_id}"

    ydl_opts = {
        "concurrent_fragment_downloads": 7,
        # "outtmpl": f"{output_path}/%(title)s.%(ext)s",
        "outtmpl": f"{output_path}/{sanitize_new_title}.%(ext)s",
        "format": "worstvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
            
            # Get the old file name
            old_file_name = f"{output_path}/{sanitize_new_title}.mp4"
            # Create the new file name
            new_title = get_clean_title(sanitize_new_title)
            new_file_name = f"{output_path}/{new_title}.mp4"
            # Rename the file
            os.rename(old_file_name, new_file_name)
            print(f"Downloaded and renamed: {new_title}")
        except yt_dlp.utils.ExtractorError as err:
            print(f"Extractor error: {err}")
    
    return new_title