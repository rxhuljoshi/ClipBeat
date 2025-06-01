import subprocess
import uuid
import os
import re
import json

previous_audio_file = None

def normalize_url(url):
    match = re.search(r"(?:youtube\.com/shorts/|youtu\.be/)([\w\-]+)", url)
    if match:
        video_id = match.group(1)
        return f"https://www.youtube.com/watch?v={video_id}"
    return url

def clean_tmp_folder():
    tmp_dir = "tmp"
    if os.path.exists(tmp_dir):
        for f in os.listdir(tmp_dir):
            if f.endswith(".mp4") or f.endswith(".mp3"):
                os.remove(os.path.join(tmp_dir, f))
    else:
        os.makedirs(tmp_dir)

def get_video_title_from_json(json_data, platform):
    try:
        data = json.loads(json_data)
        if platform == "youtube":
            return data.get("title", f"video_{str(uuid.uuid4())}")
        elif platform == "instagram":
            uploader = data.get("uploader", "insta_user")
            return f"{uploader} - Insta Reel"
    except Exception:
        return f"video_{str(uuid.uuid4())}"

def download_audio(url):
    global previous_audio_file
    url = normalize_url(url)
    os.makedirs("tmp", exist_ok=True)

    if previous_audio_file and os.path.exists(previous_audio_file):
        os.remove(previous_audio_file)

    info_command = [
        "yt-dlp",
        "--dump-json",
        "-f", "bestaudio",
        url
    ]

    try:
        result_info = subprocess.run(info_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result_info.returncode != 0:
            print("[ERROR] Failed to get metadata")
            return None, None

        data = json.loads(result_info.stdout)

        is_youtube = "youtube.com" in url or "youtu.be" in url
        if is_youtube:
            title = data.get("title", f"audio_{str(uuid.uuid4())}")
        else:
            uploader = data.get("uploader", "insta_user")
            title = f"{uploader} - Insta Reel"

        safe_title = re.sub(r'[\\/*?:"<>|]', "", title)
        mp3_path = f"tmp/{safe_title}.mp3"

        command = [
            "yt-dlp",
            "-f", "bestaudio",
            "--extract-audio",
            "--audio-format", "mp3",
            "--output", mp3_path,
            url
        ]

        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)

        if result.returncode == 0 and os.path.exists(mp3_path):
            previous_audio_file = mp3_path
            return mp3_path, f"{safe_title}.mp3"
        else:
            return None, None

    except Exception as e:
        print(f"[ERROR] {e}")
        return None, None

def download_video(url, quality="bestvideo+bestaudio/best"):
    clean_tmp_folder()

    url = normalize_url(url)
    is_youtube = "youtube.com" in url or "youtu.be" in url
    is_instagram = "instagram.com" in url

    info_command = [
        "yt-dlp",
        "--dump-json",
        "-f", quality,
        url
    ]

    try:
        result_info = subprocess.run(info_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result_info.returncode != 0:
            print("[ERROR] Failed to get metadata")
            return None, None

        title = get_video_title_from_json(result_info.stdout, "youtube" if is_youtube else "instagram")
        safe_title = re.sub(r'[\\/*?:"<>|]', "", title)
        video_path = f"tmp/{safe_title}.mp4"

        command = [
            "yt-dlp",
            "-f", quality,
            "--merge-output-format", "mp4",
            "-o", video_path,
            url
        ]

        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)

        if result.returncode == 0 and os.path.exists(video_path):
            return video_path, f"{safe_title}.mp4"
        else:
            return None, None

    except Exception as e:
        print(f"[ERROR] {e}")
        return None, None