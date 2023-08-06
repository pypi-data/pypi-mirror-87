"""CLI entrypoint for the playlist downloader"""
import argparse

import yt_playlist_dl


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Download youtube playlists'
    )

    parser.add_argument(
        'urls',
        nargs='+',
        help='URL(s) of the youtube playlist'
    )

    args = parser.parse_args()
    yt_playlist_dl.download_videos(args.urls)
