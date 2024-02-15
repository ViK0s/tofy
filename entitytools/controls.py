from pyglet import event

#handle controls and turns using publisher/subscriber design pattern



class PlayerControls(event.EventDispatcher):
    def control(self):
        self.dispatch_event("on_key")


