from video_server import VideoServer

def main():
    video_server = VideoServer()

    video_id = input("Enter video ID to play (1, 2, or 3): ")

    video = video_server.get_video(video_id)

    if video:
        video.play()

if __name__ == "__main__":
    main()
