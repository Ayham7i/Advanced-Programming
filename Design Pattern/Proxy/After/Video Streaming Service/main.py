from video_proxy import VideoProxy

def main():
    video_proxy = VideoProxy()

    video_id = input("Enter video ID to play (1, 2, or 3): ")

    video = video_proxy.get_video(video_id)

    if video:
        video.play()

if __name__ == "__main__":
    main()
