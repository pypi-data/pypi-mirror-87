import asyncio
from random import randint
from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from eventipy.event import Event
from eventipy.event_stream import EventStream

events: EventStream
event: Event


@pytest.fixture(autouse=True)
def run_around_tests():
    global events, event
    events = EventStream()
    event = Event(str(uuid4()))
    yield


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


def test_subscribe():
    topic = str(uuid4())

    @events.subscribe(topic)
    def handler(received_event: Event):
        return received_event.id

    assert handler(event) == event.id
    assert isinstance(events.subscribers[topic], list)


def test_subscribe_event_published():
    @events.subscribe(event.topic)
    def handler(received_event: Event):
        return received_event.id

    events.subscribers[event.topic][0] = MagicMock()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    events.subscribers[event.topic][0].return_value = asyncio.Future()
    events.publish(event)
    events.subscribers[event.topic][0].assert_called_with(event)


def test_add_subscriber():
    events._add_subscriber(event.topic, lambda x: x)
    assert len(events.subscribers[event.topic]) == 1
    events._add_subscriber(event.topic, lambda x: x)
    assert len(events.subscribers[event.topic]) == 2
