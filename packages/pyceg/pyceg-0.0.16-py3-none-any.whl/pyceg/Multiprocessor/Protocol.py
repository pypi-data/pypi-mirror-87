from pyceg.Multiprocessor.Processor import Processor
from pyceg.Multiprocessor.Operations import MESIOps as Ops
from pyceg.Multiprocessor.States import MOESIState as State, VIState
from pyceg.Multiprocessor.Statistics import Statistics
from tabulate import tabulate


class Protocol:
    def __init__(self, n_processors=2, memory_content=None):
        self.processors = [Processor(pid=i + 1) for i in range(n_processors)]
        self.memory_content = memory_content
        # Storing Statistical Parameters
        self.stats = Statistics()
        # Additional Private Variables
        self.modified_value = None
        self.history = []

    def __repr__(self):
        return tabulate(self.history, headers=self.get_headers(), stralign="center", numalign="center")

    def __str__(self):
        return tabulate(self.history, headers=self.get_headers(), stralign="center", numalign="center")

    def on_event(self, pid, event, function):
        if event == Ops.PrRd:
            self.stats.n_reads += 1
        elif event == Ops.PrWr:
            self.stats.n_writes += 1
        state = self.get_processor_state(pid)
        if state == State.I:
            states = {p.state for p in self.other_processors_not(pid=pid)}
            if len(states) == 1 and State.I in states:
                self.stats.n_cache_misses += 1
            if State.S in states:
                self.stats.n_cache_misses += 1
            if states.intersection({State.M, State.E, State.O}):
                self.stats.n_cache_to_cache_transfers += 1
        return ''

    def on_post_event(self, pid, event, function):
        """
        Perform Post Event Logic, to set Processor's Cache and Memory Content
        """
        state = self.get_processor_state(pid)
        # Processor Write to Cache using an Operation
        if event == Ops.PrWr:
            self.perform_processor_operation(pid, function)

        # Self Invalidate
        if event == Ops.PrInv:
            self.set_processor_state(pid, "I")
            self.set_processor_cache_content(pid, None)

        # Invalidate copy
        if event in (Ops.BusUpgr, Ops.BusRdX):
            self.set_processor_cache_content(pid, None)

        # If the new state is modified, store the modified value
        if state in (State.M, VIState.V):
            self.modified_value = self.get_processor_cache_content(pid)

        # Processor Read/Write from Memory
        if event in (Ops.PrRd, Ops.PrWr):
            cache_content = self.modified_value or self.memory_content
            self.set_processor_cache_content(pid, cache_content)

    def all_processors_are_invalid(self):
        """ MESI Extensions"""
        return all(p.state == State.I for p in self.processors)

    def processor(self, pid):
        return self.processors[pid - 1]

    def other_processors_not(self, pid):
        """Gets the list of other processors which are not equal to pid"""
        return [p for p in self.processors if p.pid != pid]

    def get_processor_state(self, pid):
        return self.processor(pid).state

    def set_processor_state(self, pid, state):
        if self.processor(pid).state != state:
            self.stats.n_state_changes += 1
            if state == "I": self.stats.n_invalidations += 1
        self.processor(pid).state = state

    def get_processor_cache_content(self, pid):
        return self.processor(pid).cache_content

    def set_processor_cache_content(self, pid, cache_content):
        self.processor(pid).cache_content = cache_content

    def perform_processor_operation(self, pid, function):
        if function and callable(function):
            cache_content = function(self.modified_value or self.get_processor_cache_content(pid) or self.memory_content)
            self.set_processor_cache_content(pid, cache_content)

    def flush(self, value):
        """"
        Request that indicates that a whole cache block is being written back to the memory
        Places the value of value of the cache line on the bus and updates the memory
        """
        self.memory_content = value
        self.stats.n_flushes += 1

    def _perform_instruction(self, pid, event, function):
        # Perform the current Processor Event
        main_transaction = self.on_event(pid, event, function)
        if main_transaction: self.stats.n_bus_latency += 1
        all_transactions = [main_transaction] if main_transaction else []
        # Update the other processors
        for processor in self.processors:
            if processor.pid != pid:
                cache_content = self.get_processor_cache_content(processor.pid)
                transaction = self.on_event(processor.pid, main_transaction, function)
                if transaction == Ops.Flush:
                    self.flush(cache_content)
                    all_transactions.append(Ops.Flush)
                if transaction: self.stats.n_bus_latency += 1

        # Save the current state into history for printing
        step_name = self.format_instruction_name(pid, event)
        self.save_history(step_name, '/'.join(all_transactions))

    def perform_instructions(self, instructions, display=True):
        for i in instructions:
            pid, operation, function = i[0], i[1], i[2] if len(i) == 3 else None
            self._perform_instruction(pid, operation, function)
        if display: print(self, '\n')

    ###########################
    # Display
    ###########################
    def get_headers(self):
        headers = ["Step"]
        [headers.extend(["P{} State".format(i + 1), "P{} Cache".format(i + 1)]) for i, p in enumerate(self.processors)]
        headers.extend(["Memory Content", "Bus Transaction", "Modified"])
        return headers

    def save_history(self, step_name, transaction):
        fields = [step_name]
        [fields.extend([p.state, p.cache_content or '-']) for p in self.processors]
        fields.extend([self.memory_content or '-', transaction or '-', self.modified_value or '-'])
        self.history.append(fields)

    ###########################
    # API Interface
    ###########################
    def api(self):
        """Protocol API Interface"""
        return {"title": self.get_headers(), "results": [item[:-1] for item in self.history], "table": str(self), "stats": self.statistics()}

    ###########################
    # Statistical Methods
    ###########################
    def statistics(self):
        return {"Instructions:": self.step_count(), **self.stats.info()}

    ###########################
    # Additional Helper Methods
    ###########################
    def step_count(self):
        return len(self.history)

    def format_instruction_name(self, processor_id, event):
        return "{}. P{} {}".format(self.step_count() + 1, processor_id, event)

    @staticmethod
    def format_instruction_set(func_name):
        if not func_name: return ""
        code = __import__("inspect").getsourcelines(func_name)[0][0].strip()
        return code.replace("(", "").replace(")", "").split(",")[2].strip().split("lambda ")[1]

    def print(self, _filter=None):
        filter_dict = {"cache": lambda v: v[:1] + v[1:][:-3:2], "cache-transaction": lambda v: filter_dict["cache"](v) + [v[-2]]}
        _filter = filter_dict.get(_filter, lambda x: x)
        headers, history = _filter(self.get_headers()), [_filter(x) for x in self.history]
        print(tabulate(history, headers=headers, stralign="center", numalign="center"))
