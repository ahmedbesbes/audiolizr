import requests
import streamlit as st
from pytube import YouTube
from streamlit_player import st_player


url = st.text_input("Enter a video URL")
PREDICTION_ENDPOINT = "http://localhost:3000/process_youtube_url"


@st.cache(allow_output_mutation=True, show_spinner=False)
def predict(url):
    response = requests.post(
        PREDICTION_ENDPOINT,
        json={"url": url},
    )
    response = response.json()
    print(response)
    return response


if url != "":
    st_player(url=url)

    youtube = YouTube(url)

    if youtube.length > 60 * 10:
        st.error("The video is too long: it must not exceed 6 min")
        st.stop()

    path = youtube.streams.filter(only_audio=True)[0].download(
        filename="/tmp/output.mp4",
    )

    with open("/tmp/output.mp4", "rb") as f:
        bytes_data = f.read()

    st.markdown("### Extracted Audio")
    st.audio(bytes_data)

    with st.spinner("Running audiolizr ..."):
        response = predict(url)
        transcript = response["transcript"]
        keywords = response["metadata"]["keywords"]
        keywords = list(map(lambda t: t[0], keywords))
        entities = response["metadata"]["entities"]
        summary = response["metadata"]["summary"]

    with st.expander("Transcript", expanded=True):
        st.markdown(transcript)

    st.markdown("### Metadata")

    with st.expander("Summary", expanded=True):
        st.write(summary)

    with st.expander("Keywords", expanded=True):
        st.write(keywords)

    with st.expander("Named entities", expanded=True):
        st.write(entities)
