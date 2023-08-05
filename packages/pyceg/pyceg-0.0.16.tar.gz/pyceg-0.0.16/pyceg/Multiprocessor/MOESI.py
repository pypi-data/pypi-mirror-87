# Basic MOESI Write-back Invalidation Protocol
from pyceg.Multiprocessor.Protocol import Protocol
from pyceg.Multiprocessor.States import MOESIState as State
from pyceg.Multiprocessor.Operations import MSIOps as Ops


###################
# MOESI Protocol
###################
class MOESI(Protocol):
    def __init__(self, n_processors=2, memory_content=None):
        super(MOESI, self).__init__(n_processors, memory_content)

    def on_event(self, pid, event, function):
        super().on_event(pid, event, function)
        state, transaction = self.get_processor_state(pid), None

        # Next State Logic
        if state == State.M:
            if event == Ops.BusRd:
                state = State.O
                transaction = Ops.Flush
            elif event == Ops.BusRdX:
                state = State.I
                transaction = Ops.Flush

        elif state == State.O:
            if event == Ops.BusRd:
                transaction = Ops.Flush
            elif event == Ops.PrWr:
                state = State.M
                transaction = Ops.BusUpgr
            elif event in (Ops.BusUpgr, Ops.BusRdX):
                state = State.I
                if event == Ops.BusRdX:
                    transaction = Ops.Flush

        elif state == State.E:
            if event == Ops.PrWr:
                state = State.M
            elif event == Ops.BusRd:
                state = State.O
                transaction = Ops.Flush
            elif event == Ops.BusRdX:
                state = State.I
                transaction = Ops.Flush

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
    moesi = MOESI(n_processors=4, memory_content=0)
    moesi.perform_instructions(instructions)
    # moesi.print(_filter="transaction")


######################
# Example 2
######################
def example2():
    instructions = [
        (1, Ops.PrRd),
        (2, Ops.PrRd),
        (3, Ops.PrWr, lambda a: a + 2),
        # (2, Ops.PrWr, lambda a: a + 2),
        # (1, Ops.PrWr, lambda a: a + 2),
        # (1, Ops.PrRd),
    ]
    moesi = MOESI(n_processors=3, memory_content=1)
    moesi.perform_instructions(instructions)
    # moesi.print(_filter="transaction")


###################
# Main
###################
# example1()
# example2()
# example2()
