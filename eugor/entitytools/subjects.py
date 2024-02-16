from pyglet import event

#handle controls and turns using publisher/subscriber design pattern


# the main subject class, subjects should be created from it so you can create your own events for your classes
class Subject(event.EventDispatcher):
    def __init__(self) -> None:
        super().__init__()
    def tick():
        pass

# i thought about just making this one main "subject class" but not only is it only boilerplate, but also pretty useless alone
# that's why I think a good idea would be to create some subjects that pretty much are always needed and could be automatically attached to some premade objects


class PlayerControls(Subject):
    def control(self):
        self.dispatch_event("on_end_turn")


class TurnEnd(Subject):
    def __init__(self):
        self.subscriberlist = []
