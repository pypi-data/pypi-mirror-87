"""Youtube Playlist downloader"""
from typing import List
import youtube_dl


def download_playlists(urls: List[str]) -> None:
    """Downloads all video URLs provided"""
    with youtube_dl.YoutubeDL({
        "outtmpl": "%(playlist_title)s/%(title)s <%(id)s>.%(ext)s"
    }) as ydl:
        ydl.download(urls)
