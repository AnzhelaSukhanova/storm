import hashlib
import io

TRACE_FILE = '.z3-trace'
trace_offset = 0


def reset_trace_offset():
    global trace_offset
    with open(TRACE_FILE, 'r') as trace:
        trace_offset = trace.seek(0, io.SEEK_END)


class TraceStats(object):

    def __init__(self):
        self.hash = 0

    def read_from_trace(self):
        with open(TRACE_FILE, 'r') as trace:
            trace.seek(trace_offset)
            lines = trace.readlines()
        if lines:
            self.load_states(lines)

    def load_states(self, states: list):
        hash_builder = hashlib.sha512()
        for state in states:
            hash_builder.update(state.encode('utf-8'))

        self.hash = hash_builder.digest()
