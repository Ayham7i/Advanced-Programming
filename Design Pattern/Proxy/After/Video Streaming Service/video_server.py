from video import Video
import time

class VideoServer:
    def __init__(self):
        self.videos = {
            
            "1": Video("Learn Python", 30),
            "2": Video("Design Patterns in Python", 45),
            "3": Video("Advanced Python Programming", 60),
        }

    def get_video(self, video_id):
        print(f"Fetching video {video_id} from server...")
        time.sleep(2)  
        video = self.videos.get(video_id)
        if not video:
            print(f"Video with ID {video_id} not found.")
        return video
