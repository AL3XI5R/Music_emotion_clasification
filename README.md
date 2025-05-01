# Music_emotion_clasification
Python program that creates an Artifical Intelligence to guess the human emotion inside of a song without using lyrics

Currently, the program isn't working with .WAV files, only MP3. Meaning that the recording function is still on progress
To May 2025 the PKL model has an accuracy of 49% in its predictions

-Page_deployment.py is the only way to visualize and use the AI, it uses Streamlit in a localhost sever
-Download_music.py connects to yt-dlp to download Youtube videos and convert them to MP3 format, needs the URLs of the videos in a file named "songs.txt"
-Create_dataset.py trains the AI and creates the CSV with ~300 files and their features using data augmentation, for each song in the file it will create two more versions, one with two semitones up and the other two semitones down

-Music_emotion_model.pkl is the AI itself
-Dataset_music_emotions.csv is the dataset with the songs and their features
