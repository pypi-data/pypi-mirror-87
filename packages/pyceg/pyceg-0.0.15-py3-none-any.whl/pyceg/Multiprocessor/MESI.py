# Basic MESI Write-back Invalidation Protocol
from pyceg.Multiprocessor.Protocol import Protocol
from pyceg.Multiprocessor.States import MESIState as State
from pyceg.Multiprocessor.Operations import MSIOps as Ops


###################
# MESI Protocol
###################
class MESI(Protocol):
    def __init__(self, n_processors=2, memory_content=None):
        super(MESI, self).__init__(n_processors, memory_content)

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

        # Perform Post Event Logic, to set Processor's Cache and Memory Content
        super().on_post_event(pid=pid, event=event, function=function)

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
    mesi = MESI(n_processors=4, memory_content=0)
    mesi.perform_instructions(instructions)
    mesi.print(_filter="cache-transaction")


###################
# Main
###################
# example1()
# example2()
