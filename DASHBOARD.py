import streamlit as st
from VAULT import analyze_video

st.title("📚 LectureVault ")
import json

with open("history.json", "r") as file:
    history = json.load(file)

st.header("Dashboard")

st.write("Total Lectures:", len(history))

if history:
    st.write("Last Studied:", history[-1]["title"])

url = st.text_input("Paste YouTube URL")
if st.button("Go"):
    try:
    
        with st.spinner("Analyzing lecture..."):
            result = analyze_video(url)
            st.header(result["title"])

            st.subheader("Subject")
            st.write(result["subject"])

            st.subheader("Chapter")
            st.write(result["chapter"])

            st.subheader("Topic")
            st.write(result["topic"])

            st.subheader("Key Points")
            for point in result["key_points"]:
                st.write("•", point)

            st.subheader("Next Topic")
            st.write(result["next_topic"])
        st.success("Video Added!")
    except Exception as e:

        st.error(e)