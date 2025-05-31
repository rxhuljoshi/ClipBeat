import streamlit as st
from utils.download import download_audio
import os

st.set_page_config(page_title="Clip Beat", page_icon="🎶")

st.title("🎶 Clip Beat")
st.caption("Instagram Reels or YouTube Shorts to MP3 Converter")

url = st.text_input("Paste Instagram Reel or YouTube Short URL")

if st.button("Find Song"):
    if url:
        with st.spinner("Downloading and extracting audio..."):
            audio_file = download_audio(url)
            if audio_file and os.path.exists(audio_file):
                st.success("Click on the three dots and then 'Download' to save the audio file.")
                st.audio(audio_file)
            else:
                st.error("Failed to download audio. Check the URL.")
    else:
        st.warning("Please paste a valid URL.")