from utils.download import download_audio

url = "https://youtube.com/shorts/dBgnz2iriCU?si=xOXOtvJDtUMmWPuj"
path = download_audio(url)

print("Downloaded to:", path)