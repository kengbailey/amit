import yt_dlp
import whisper
import sqlite3
from datetime import datetime


def youtube_to_m4a(url_list):
    """
    Downloads the audio from YouTube videos in the given URL list and saves them as M4A files.

    Args:
        url_list (list): A list of YouTube video URLs.

    Returns:
        None
    """
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
        }]
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for url in url_list:
            error_code = ydl.download([url])

def create_amit_db():
    """
    Function to create the amit database and the llm_analysis table.
    """
    conn = sqlite3.connect('./data/amit.db')
    c = conn.cursor()

    # Create ll_analysis table
    c.execute('''CREATE TABLE IF NOT EXISTS llm_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prompt_text TEXT NOT NULL,
                llm_params TEXT NOT NULL,
                output_text TEXT NOT NULL,
                output_stats TEXT,
                context TEXT,
                date_created DATETIME DEFAULT CURRENT_TIMESTAMP)''')

    # Create episode transcripts table
    c.execute('''CREATE TABLE IF NOT EXISTS video_transcription (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                transcription TEXT NOT NULL,
                url TEXT NOT NULL,
                context TEXT,
                date_created DATETIME DEFAULT CURRENT_TIMESTAMP
                );''')

    conn.commit()
    conn.close()

def m4a_to_text(m4a_file):
    """
    Transcribes the audio from an M4A file to text.

    Args:
        m4a_file (str): The path to the M4A file.

    Returns:
        str: The text transcription of the M4A file.
    """
    model = whisper.load_model("base.en")
    result = model.transcribe(m4a_file)
    return result["text"]

def insert_video_transcription(filename, transcription, context):
    """
    Inserts a video transcription into the database.

    Args:
        filename (str): The name of the video file.
        transcription (str): The transcription of the video.
        url (str): The youtube url of the video.

    Returns:
        None
    """
    conn = sqlite3.connect('./data/amit.db')
    c = conn.cursor()
    sql = """INSERT INTO video_transcription (filename, transcription, url) 
    VALUES (?, ?, ?)"""
    c.execute(sql, (filename, transcription, context))
    conn.commit()
    conn.close()

if __name__ == '__main__':

    # youtube_to_m4a(["https://www.youtube.com/watch?v=5AU2beqDoDY"])

    # create_amit_db()

    m4a_file = "data/wheeling_options_001_010324.m4a"
    result = m4a_to_text(m4a_file)
    insert_video_transcription(m4a_file, result, "https://www.youtube.com/watch?v=5AU2beqDoDY")
    