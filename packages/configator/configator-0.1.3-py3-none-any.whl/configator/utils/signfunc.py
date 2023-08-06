#!/usr/bin/env python3

import logging
import signal
import threading

LOG = logging.getLogger(__name__)

def hook_signal(reaction, signal_code=signal.SIGINT, finished=False):
    if not threading.current_thread() is threading.main_thread():
        return None
    current_handler = None
    def signal_handler(signalnum, frame):
        if LOG.isEnabledFor(logging.DEBUG):
            LOG.log(logging.DEBUG, "SIGNAL[%d] received" % signalnum)
        #
        reaction()
        #
        if not finished and callable(current_handler):
            if LOG.isEnabledFor(logging.DEBUG):
                LOG.log(logging.DEBUG, "Invoke the default handler")
            current_handler(signalnum, frame)
    current_handler = signal.signal(signal_code, signal_handler)
    return None
