import hashlib
import io

TRACE_FILE = '.z3-trace'
trace_offset = 0


class State(object):

    def __init__(self, line: str):
        parts = line.rstrip().split('/')
        self.name = parts[0].split('..')[0]  # function
        self.name += parts[-1]  # file:line

    def __eq__(self, other):
        if self.name != other.name:
            return False
        return True

    def __hash__(self):
        return hash(self.name)

    def encode(self, standart: str):
        return self.name.encode(standart)

    def save(self):
        return self.name

    @staticmethod
    def load(data) -> 'State':
        state = State('')
        state.name = data
        return state


def reset_trace_offset():
    global trace_offset
    with open(TRACE_FILE, 'r') as trace:
        trace_offset = trace.seek(0, io.SEEK_END)


class TraceStats(object):

    def __init__(self):
        self.states = []
        self.hash = 0

    def read_from_trace(self):
        with open(TRACE_FILE, 'r') as trace:
            trace.seek(trace_offset)
            lines = trace.readlines()
        self.states = [State(line) for line in lines]
        if self.states:
            self.load_states()

    def load_states(self):
        hash_builder = hashlib.sha512()
        for state in self.states:
            hash_builder.update(state.encode('utf-8'))

        self.hash = hash_builder.digest()
