from typing import Callable, Dict, List, Any
from Enums import EventTypes

class EventBus:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EventBus, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        self._initialized = True
        self._subscribers: Dict[EventTypes, List[Callable[[Dict[str, Any]], None]]] = {}

    def subscribe(self, event_type: EventTypes, callback: Callable[[Dict[str, Any]], None]):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)

    def unsubscribe(self, event_type: str, callback: Callable[[Dict[str, Any]], None]):
        if event_type in self._subscribers:
            self._subscribers[event_type].remove(callback)

    def publish(self, event_type: EventTypes, data: Dict[str, Any] = None):
        if data is None:
            data = {}
        data['event_type'] = event_type
        if event_type in self._subscribers:
            for callback in self._subscribers[event_type]:
                callback(data)
