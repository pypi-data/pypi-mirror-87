import asyncio
from random import randint
from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from eventipy.event import Event
from eventipy.event_stream import EventStream, ALL_TOPICS

events: EventStream
event: Event


@pytest.fixture(autouse=True)
def run_around_tests():
    global events, event
    events = EventStream()
    event = Event(str(uuid4()))
    yield


def assert_topic_handlers_were_called(topic: str):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    for index in range(len(events.subscribers[topic])):
        handler = MagicMock()
        handler.return_value = asyncio.Future()
        events.subscribers[topic][index] = handler

    events.publish(event)
    for handler in events.subscribers[topic]:
        handler.assert_called_with(event)


def test_publish():
    events.publish(event)
    assert events[0] == event


def test_publish_integer():
    with pytest.raises(TypeError):
        events.publish(0)


def test_set_item():
    events.publish(event)
    with pytest.raises(TypeError):
        events[0] = event


def test_get_all_events_by_topic():
    amount_of_events = randint(1, 30)
    topic = str(uuid4())

    for _ in range(amount_of_events):
        events.publish(Event(topic))

    topic_events = events.get_by_topic(topic=topic)

    assert len(topic_events) == amount_of_events
    matching_topic_events = [topic_event
                             for topic_event in topic_events
                             if topic_event.topic == topic]

    assert len(matching_topic_events) == len(topic_events)


def test_get_five_events_by_topic():
    amount_of_events = randint(1, 30)
    max_events = randint(1, amount_of_events)
    topic = str(uuid4())

    for _ in range(amount_of_events):
        events.publish(Event(topic))

    topic_events = events.get_by_topic(topic=topic, max_events=max_events)

    assert len(topic_events) == max_events
    matching_topic_events = [topic_event
                             for topic_event in topic_events
                             if topic_event.topic == topic]

    assert len(matching_topic_events) == len(topic_events)


def test_get_by_id():
    events.publish(event)
    assert events.get_by_id(event.id) == event


def test_subscribe_with_decorator():
    topic = str(uuid4())

    @events.subscribe(topic)
    def handler(received_event: Event):
        return received_event.id

    assert handler(event) == event.id
    assert isinstance(events.subscribers[topic], list)


def test_subscribe_without_decorator():
    topic = str(uuid4())

    def handler(received_event: Event):
        return received_event.id

    events.subscribe(topic, handler)

    assert handler(event) == event.id
    assert isinstance(events.subscribers[topic], list)


def test_subscribe_with_decorator_event_published():
    @events.subscribe(event.topic)
    def handler(received_event: Event):
        return received_event.id

    assert_topic_handlers_were_called(event.topic)


def test_subscribe_without_decorator_event_published():
    def handler(received_event: Event):
        return received_event.id

    events.subscribe(event.topic, handler)
    assert_topic_handlers_were_called(event.topic)


def test_subscribe_to_all_topics():
    @events.subscribe_to_all
    def handler(received_event: Event):
        return received_event.id

    assert_topic_handlers_were_called(ALL_TOPICS)


def test_subscribe_to_all_without_decorator_topics():
    def handler(received_event: Event):
        return received_event.id

    events.subscribe_to_all(event_handler=handler)
    assert_topic_handlers_were_called(ALL_TOPICS)


def test_add_subscriber():
    events._add_subscriber(event.topic, lambda x: x)
    assert len(events.subscribers[event.topic]) == 1
    events._add_subscriber(event.topic, lambda x: x)
    assert len(events.subscribers[event.topic]) == 2
