from yt_dlp import YoutubeDL

def get_clean_title(video_title):
    ascii_title = video_title.encode('ascii', errors='ignore').decode()
    clean_title = ''.join(ch for ch in ascii_title if ch.isalnum())
    return clean_title
