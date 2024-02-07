class ResizeTracker:
    
    def __init__(self, frame):
            self.frame = frame
            self.width = frame.winfo_width()
            self.height = frame.winfo_height()
            frame.bind("<Configure>", self.resize)

    def resize(self, event):
        if (event.widget == self.frame) and (self.width != event.width or self.height != event.height):
            self.width = event.width
            self.height = event.height
            self.frame.dimensions = (self.width, self.height)
            self.frame.initialize_draw_constants()
            self.frame.draw()