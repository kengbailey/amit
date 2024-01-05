import yt_dlp


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



if __name__ == '__main__':
    youtube_to_m4a()

"""
What are we doing today? 
sqlite storage of analysis
versioned analysis
put functions into this file
entire process we've laid out so far
"""