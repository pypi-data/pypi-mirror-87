"""Youtube Playlist downloader"""
import youtube_dl


def download_videos(urls) -> None:
    with youtube_dl.YoutubeDL() as ydl:
        ydl.download(urls)


def main() -> None:
    download_videos(['https://www.youtube.com/watch?v=E2lvxFANg4U'])
