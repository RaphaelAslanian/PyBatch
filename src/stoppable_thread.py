from threading import Event


class StoppableThread   :

    def __init__(self, setted: bool):
        self.stop_event = Event()
        if setted:
            self.stop_event.set()
        else:
            self.stop_event.clear()
