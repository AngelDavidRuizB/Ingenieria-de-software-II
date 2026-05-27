class EventBus:
    _instance = None
    _subscribers: dict

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._subscribers = {}
        return cls._instance

    def subscribe(self, event_type, subscriber):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(subscriber)

    def unsubscribe(self, event_type, subscriber):
        if event_type in self._subscribers:
            self._subscribers[event_type].remove(subscriber)

    def publish(self, event_type, data):
        if event_type in self._subscribers:
            for subscriber in self._subscribers[event_type]:
                subscriber.update(event_type, data)
