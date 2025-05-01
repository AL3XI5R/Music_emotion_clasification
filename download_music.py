#Download the URL list from the text file and convert to mp3
#Use "Clean link" from Youtube in the text file


import os
import subprocess

#New folder for downloaded songs
output_folder = "Downloaded_Songs"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)


songs_file = r{PATH WHERE THE SONGS.TXT IS LOCATED}


#Seems like without this it wont work :///
ffmpeg_path = r"C:\ffmpeg\bin" #<== IF YOUR FFMPEG IS IN ANOTHER LOCATION, INDICATE SO

#Download and convert
subprocess.run([
    "yt-dlp",
    "-x",
    "--audio-format", "mp3",
    "--audio-quality", "192K",
    "--ffmpeg-location", ffmpeg_path,
    "-o", "Downloaded_Songs/%(title)s.%(ext)s",
    "-a", songs_file
])
