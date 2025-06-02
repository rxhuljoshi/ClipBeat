import streamlit as st
from utils.download import download_audio, download_video
import os

st.set_page_config(page_title="Clip Beat", page_icon="🎶", layout="centered")

if "mode" not in st.session_state:
    st.session_state.mode = "audio"
if "video_path" not in st.session_state:
    st.session_state.video_path = None
if "video_filename" not in st.session_state:
    st.session_state.video_filename = None

st.title("Clip Beat")
st.caption("Convert Instagram Reels and YouTube Shorts to Audio or Video")

tab1, tab2 = st.tabs(["🎵 Audio", "🎬 Video"])

with tab1:
    st.subheader("Audio Downloader")
    audio_url = st.text_input("Paste Instagram Reel or YouTube Short URL", key="audio_url")

    if st.button("Find Song"):
        if audio_url:
            with st.spinner("Downloading and converting to MP3..."):
                audio_path, audio_filename = download_audio(audio_url)
                if audio_path and os.path.exists(audio_path):
                    with open(audio_path, "rb") as f:
                        st.audio(f, format="audio/mp3", start_time=0)
                        st.download_button("Download Audio", f, file_name=audio_filename, mime="audio/mpeg")
                else:
                    st.error("Failed to download audio. Check the URL.")
        else:
            st.warning("Please paste a valid URL.")

with tab2:
    st.subheader("Video Downloader")
    video_url = st.text_input("Paste Instagram Reel or YouTube Short URL", key="video_url")

    quality = st.selectbox("Select Video Quality", ["1080p", "720p", "480p", "360p"])
    quality_map = {
        "1080p": "bestvideo[height<=1080]+bestaudio/best",
        "720p": "bestvideo[height<=720]+bestaudio/best",
        "480p": "bestvideo[height<=480]+bestaudio/best",
        "360p": "bestvideo[height<=360]+bestaudio/best",
    }

    if st.button("Find Video"):
        if video_url:
            with st.spinner("Downloading video..."):
                selected_quality = quality_map[quality]
                video_path, video_filename = download_video(video_url, selected_quality)
                if video_path and os.path.exists(video_path):
                    st.session_state.video_path = video_path
                    st.session_state.video_filename = video_filename
                    st.success("Video downloaded successfully!")
                else:
                    st.error("Failed to download video. Check the URL.")
        else:
            st.warning("Please paste a valid URL.")

    if st.session_state.video_path and os.path.exists(st.session_state.video_path):
        st.video(st.session_state.video_path)
        with open(st.session_state.video_path, "rb") as f:
            st.download_button("Download Video", f, file_name=st.session_state.video_filename, mime="video/mp4")