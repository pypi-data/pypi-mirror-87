
import logging
import signal
import threading

def hook_signal(self, signal_code, reaction, finished=False):
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
