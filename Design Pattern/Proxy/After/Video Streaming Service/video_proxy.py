from video_server import VideoServer

class VideoProxy:
    def __init__(self):
        self.server = VideoServer()
        self.cache = {}

    def get_video(self, video_id):
        
        if video_id in self.cache:
            print(f"Returning cached video {video_id}")
            return self.cache[video_id]
        
        video = self.server.get_video(video_id)
        if video:
            self.cache[video_id] = video
        return video
