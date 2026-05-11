from src.services.signal_poller import (
    SignalPoller
)

poller = (
    SignalPoller()
)

poller.start()