"""Exceptions.py
This file defines all the exceptions used by the library."""

class InitializationTimeout(Exception):
    """Called when the initialization of the websocket exceeds the timeout."""
    pass

class RetrievalTimeout(Exception):
    """Called when the retrieval of menu data exceeds the timeout."""
    pass

class InvalidSubscriptionType(Exception):
    """Called when the user entered invalid events to subscribe to."""
    pass