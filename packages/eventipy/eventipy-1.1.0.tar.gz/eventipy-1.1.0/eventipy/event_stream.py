import asyncio
import logging
from collections.abc import Sequence
from functools import wraps
from typing import List, Callable, Dict
from uuid import UUID

from eventipy.event import Event
from eventipy.event_handler import EventHandler

logger = logging.getLogger(__name__)


class EventStream(Sequence):
    def __init__(self):
        self.__events: List[Event] = []
        self.subscribers: Dict[str, List[Callable]] = {}

    def publish(self, event: Event) -> None:
        """
        Args:
            event (Event): The event to publish
        """

        if not isinstance(event, Event):
            raise TypeError("event must be of type Event")

        if self.get_by_id(event.id):
            raise ValueError(f"event with {event.id} already written")

        self.__events.append(event)
        asyncio.run(self._publish_to_subscribers(event))

    async def _publish_to_subscribers(self, event: Event) -> None:
        try:
            for handler in self.subscribers[event.topic]:
                # Ensure handler is called, but don't wait for result
                asyncio.ensure_future(handler(event))
        except KeyError:
            pass

    def subscribe(self, topic: str, event_handler: EventHandler = None) -> Callable:
        """
        Args:
            topic (str): The topic to which this handler listens
            event_handler (Callable[[Event], None]): Optional handler to give to avoid using decorator
        """

        def wrapper(event_handler: EventHandler) -> Callable:
            @wraps(event_handler)
            async def handle_event(event: Event):
                try:
                    event_handler(event)
                except Exception as exception:
                    logger.warning(f"{event_handler.__name__} failed to handle "
                                   f"event of topic {topic}. "
                                   f"Exception: {exception}")

            self._add_subscriber(topic, handler=handle_event)
            return event_handler

        if event_handler:
            return wrapper(event_handler)

        return wrapper

    def _add_subscriber(self, topic: str, handler: Callable) -> None:
        try:
            self.subscribers[topic].append(handler)
        except KeyError:
            self.subscribers[topic] = [handler]

    def get_by_id(self, event_id: UUID) -> Event:
        """
        Args:
            event_id (UUID): The id of the wanted event
        """
        for event in self.__events:
            if event.id == event_id:
                return event

    def get_by_topic(self, topic: str, max_events: int = None) -> List[Event]:
        """
        Args:
            topic (str): The topic to which the event was published
            max_events (int): The maximum number of events to retrieve
        """
        matching_events = []
        for event in self.__events:
            if event.topic == topic:
                matching_events.append(event)
            if max_events and len(matching_events) >= max_events:
                break
        return matching_events

    def __len__(self) -> int:
        return len(self.__events)

    def __getitem__(self, i: int) -> Event:
        return self.__events[i]

    def __setitem__(self, key, value) -> None:
        raise TypeError("EventStream object does not support item assignment")

    def __repr__(self) -> str:
        return repr(self.__events)

    def __str__(self) -> str:
        return str(self.__events)


events = EventStream()
