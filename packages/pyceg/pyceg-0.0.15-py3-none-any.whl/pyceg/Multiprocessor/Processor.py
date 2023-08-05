class Processor:
    def __init__(self, pid=1, state="I", cache_content=None):
        self.pid, self.state, self.cache_content = pid, state, cache_content

    def __repr__(self):
        return "PID: {} | State: {} | Cache Content: {}".format(self.pid, self.state, self.cache_content)

    def reset(self):
        self.state, self.cache_content = "I", None
