# Basic MOSI Write-back Invalidation Protocol


from Protocol import Protocol
from States import MESIState as State
from Operations import MSIOps as Ops


###################
# MOSI Protocol
###################


class MOSI(Protocol):
    def __init__(self, n_processors=2, memory_content=None):
        super(MOSI, self).__init__(n_processors, memory_content)

    # MESI Extensions
    def all_processors_are_invalid(self):
        return all(p.state == State.I for p in self.processors)

    def on_event(self, pid, event, function):
        super().on_event(pid, event, function)
        state, transaction = self.get_processor_state(pid), None

        # Next State Logic
        if state == State.M:
            if event == Ops.BusRd:
                state = State.S
                transaction = Ops.Flush
            elif event == Ops.BusRdX:
                state = State.I
                transaction = Ops.Flush

        elif state == State.E:
            if event == Ops.PrWr:
                state = State.M
            elif event == Ops.BusRd:
                state = State.S
            elif event == Ops.BusRdX:
                state = State.I

        elif state == State.S:
            if event == Ops.PrWr:
                state = State.M
                transaction = Ops.BusUpgr
            elif event in (Ops.BusUpgr, Ops.BusRdX):
                state = State.I

        elif state == State.I:
            if event == Ops.PrWr:
                state = State.M
                transaction = Ops.BusRdX
            elif event == Ops.PrRd:
                if self.all_processors_are_invalid():
                    state = State.E
                else:
                    state = State.S
                transaction = Ops.BusRd
        # Set State
        self.set_processor_state(pid, state)

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
        if state == State.M:
            self.modified_value = self.get_processor_cache_content(pid)

        # Processor Read/Write from Memory
        if event in (Ops.PrRd, Ops.PrWr):
            cache_content = self.modified_value or self.memory_content
            self.set_processor_cache_content(pid, cache_content)

        return transaction


######################
# Example 1
# DGD 5
######################
def example1():
    instructions = [
        (1, Ops.PrRd),
        (2, Ops.PrRd),
        (3, Ops.PrRd),
        (4, Ops.PrWr, lambda a: 1),
        (1, Ops.PrRd),
    ]
    mosi = MOSI(n_processors=4, memory_content=0)
    mosi.perform_instructions(instructions)
    mosi.print(_filter="transaction")

###################
# Main
###################
# example1()
# example2()
