import subprocess
import uuid
import os

previous_file = None

def normalize_url(url):
    import re
    match = re.search(r"(?:youtube\.com/shorts/|youtu\.be/)([\w\-]+)", url)
    if match:
        video_id = match.group(1)
        return f"https://www.youtube.com/watch?v={video_id}"
    return url

def download_audio(url):
    global previous_file
    url = normalize_url(url)
    os.makedirs("tmp", exist_ok=True)
    
    if previous_file and os.path.exists(previous_file):
        os.remove(previous_file)

    unique_id = str(uuid.uuid4())
    mp4_path = f"tmp/{unique_id}.mp4"

    command = [
        "yt-dlp",
        "-f", "bestaudio",
        "--output", mp4_path,
        url
    ]

    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)

        if result.returncode == 0 and os.path.exists(mp4_path):
            previous_file = mp4_path
            return mp4_path
        else:
            return None
    except Exception as e:
        print(f"[ERROR] {e}")
        return None