import pyglet



#the main observer class
class Entity(pyglet.sprite.Sprite):
    def __init__(self,*args, **kwargs):
        super(Entity, self).__init__(*args, **kwargs)
        #subject.push_handlers(self)
    def PublishTopic(TopicClass):
        TopicClass.push_handlers(TopicClass.topic)
        pass
    def SubscribeTopic(TopicClass):
        pass