import streamlit as st
from utils.download import download_audio, download_video, clear_downloads
import os

st.set_page_config(page_title="Clip Beat", page_icon="🎶", layout="centered")

if "mode" not in st.session_state:
    st.session_state.mode = "audio"

st.title("Clip Beat")
st.caption("Convert Instagram Reels and YouTube Shorts to Audio or Video")

tab1, tab2 = st.tabs(["🎵 Audio", "🎬 Video"])

with tab1:
    st.subheader("Audio Downloader")
    audio_url = st.text_input("Paste Instagram Reel or YouTube Short URL", key="audio_url")

    if st.button("Find Song"):
        if audio_url:
            with st.spinner("Downloading and converting to MP3..."):
                clear_downloads()
                audio_path, audio_filename = download_audio(audio_url)
                if audio_path and os.path.exists(audio_path):
                    st.audio(audio_path)
                    with open(audio_path, "rb") as f:
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
        "1080p": "bestvideo[height<=1080]+bestaudio/best/best",
        "720p": "bestvideo[height<=720]+bestaudio/best/best",
        "480p": "bestvideo[height<=480]+bestaudio/best/best",
        "360p": "bestvideo[height<=360]+bestaudio/best/best",
    }

    if st.button("Find Video"):
        if video_url:
            with st.spinner("Downloading video..."):
                clear_downloads()
                selected_quality = quality_map[quality]
                video_path, video_filename = download_video(video_url, selected_quality)
                if video_path and os.path.exists(video_path):
                    st.session_state.video_path = video_path
                    st.session_state.video_filename = video_filename
                else:
                    st.error("Failed to download video. Check the URL.")
        else:
            st.warning("Please paste a valid URL.")

    if "video_path" in st.session_state and st.session_state.video_path:
        st.video(st.session_state.video_path)
        with open(st.session_state.video_path, "rb") as f:
            st.download_button("Download Video", f, file_name=st.session_state.video_filename, mime="video/mp4")