class Video:
    def __init__(self, title, duration):
        self.title = title
        self.duration = duration  

    def play(self):
        print(f"Playing video: {self.title} ({self.duration} minutes)")
