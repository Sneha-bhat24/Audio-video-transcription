import streamlit as st
import whisper
import language_tool_python
from gtts import gTTS
import moviepy.editor as mp
import os

# Function to transcribe and correct
def transcribe_and_correct(file):
    # Load Whisper model
    model = whisper.load_model("base")
    
    # Transcribe audio
    result = model.transcribe(file)
    transcription = result['text']
    
    # Initialize LanguageTool
    tool = language_tool_python.LanguageTool('en-US')
    
    # Correct the transcription
    matches = tool.check(transcription)
    corrected_transcription = language_tool_python.utils.correct(transcription, matches)
    
    # Close the LanguageTool
    tool.close()

    return transcription, corrected_transcription

# Function to synthesize speech using gTTS
def synthesize_speech(text, output_file="output.mp3"):
    tts = gTTS(text=text, lang='en')
    tts.save(output_file)
    return output_file

# Function to replace video audio with AI-generated audio
def replace_audio_in_video(video_file, audio_file, output_file="final_video_with_ai_voice.mp4"):
    video = mp.VideoFileClip(video_file)
    audio = mp.AudioFileClip(audio_file)
    
    # Set new audio to the video
    final_video = video.set_audio(audio)
    
    # Save the final video
    final_video.write_videofile(output_file, codec="libx264", audio_codec="aac")
    return output_file

# Streamlit UI
st.title("Transcription and Grammar Correction with AI Voice and Video Sync")

# Upload file section
uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "wav", "mpeg4"])

if uploaded_file is not None:
    # Save the uploaded file temporarily
    video_path = "temp_file.mp4"
    with open(video_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.video(video_path)
    
    st.write("Transcribing audio...")
    
    # Transcribe and correct transcription
    original_transcription, corrected_transcription = transcribe_and_correct(video_path)
    
    # Display the results
    st.subheader("Original Transcription")
    st.write(original_transcription)

    st.subheader("Corrected Transcription")
    st.write(corrected_transcription)
    
    # Synthesize speech from corrected transcription
    st.write("Generating AI voice...")
    audio_file = synthesize_speech(corrected_transcription, "ai_generated_voice.mp3")
    
    # Play AI-generated voice
    st.subheader("AI-Generated Voice")
    st.audio(audio_file)
    
    # Replace video audio with AI voice
    st.write("Replacing video audio with AI-generated voice...")
    final_video = replace_audio_in_video(video_path, audio_file, "final_output.mp4")
    
    # Play the final video with AI voice
    st.subheader("Final Video with AI Voice")
    st.video(final_video)

    # Clean up
    os.remove(video_path)
    os.remove(audio_file)
    os.remove(final_video)
