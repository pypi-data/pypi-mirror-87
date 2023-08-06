from typing import Callable, Any

from eventipy import Event

EventHandler = Callable[[Event], Any]
