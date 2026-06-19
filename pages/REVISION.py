import streamlit as st
import json

st.title("📚 Revision Library")

with open("history.json", "r") as file:
    history = json.load(file)

library = {}
for lecture in history:

    subject = lecture["subject"]
    chapter = lecture["chapter"]

    if subject not in library:
        library[subject] = {}

    if chapter not in library[subject]:
        library[subject][chapter] = []

    library[subject][chapter].append(lecture)
for subject in library:
    
    with st.expander(subject):

        for chapter in library[subject]:

            with st.expander(chapter):

                for lecture in library[subject][chapter]:

                    with st.expander(f"📹 {lecture['title']}"):

                        st.write("**Subject:**", lecture["subject"])

                        st.write("**Chapter:**", lecture["chapter"])

                        st.write("**Topic:**", lecture["topic"])
                        st.subheader("Next Topic")
                        st.write(lecture["next_topic"])
                        st.subheader("Key Points")

                        for point in lecture["key_points"]:

                            st.write("•", point)

                        st.subheader("Date Studied")
                        st.write(lecture["date"])