#  Two-state write-through write invalidate protocol
from pyceg.Multiprocessor.Protocol import Protocol
from pyceg.Multiprocessor.States import VIState as State
from pyceg.Multiprocessor.Operations import VIOps as Ops


######################################
# Two State Protocol (VI Write Through)
######################################
class VI(Protocol):
    def __init__(self, n_processors=2, memory_content=None):
        super(VI, self).__init__(n_processors, memory_content)

    def on_event(self, pid, event, function):
        super().on_event(pid, event, function)
        state, transaction = self.get_processor_state(pid), None

        # Next State Logic
        if state == State.V:
            if event in (Ops.BusWr, Ops.BusRdX):
                state = State.I
                self.set_processor_cache_content(pid, None)
            elif event == Ops.PrWr:
                transaction = Ops.BusWr

        elif state == State.I:
            if event == Ops.PrRd:
                state = State.V
                transaction = Ops.BusRd
            elif event == Ops.PrWr:
                state = State.V
                transaction = Ops.BusWr

        # Set State
        self.set_processor_state(pid, state)

        # Perform Post Event Logic, to set Processor's Cache and Memory Content
        super().on_post_event(pid=pid, event=event, function=function)

        return transaction


#####################
# Example 1
# Zoom Lecture Nov 6
#####################
def example1():
    instructions = [
        (1, Ops.PrRd),
        (2, Ops.PrRd),
        (2, Ops.PrWr, lambda _: 10),
        (2, Ops.PrRd),
        (2, Ops.PrWr, lambda _: 15),
        (1, Ops.PrWr, lambda _: 20),
        (2, Ops.PrRd),
    ]
    vi = VI(n_processors=len(set(x[0] for x in instructions)), memory_content=5)
    vi.perform_instructions(instructions)


###################
# Example 2
# Quiz 2 2019
# Question 3
###################
def example2():
    instructions = [
        (1, Ops.PrRd),
        (2, Ops.PrRd),
        (2, Ops.PrWr, lambda x: x + 2),
        (1, Ops.PrWr, lambda x: x * 2),
        (2, Ops.PrRd),
    ]
    vi = VI(n_processors=len(set(x[0] for x in instructions)), memory_content=3)
    vi.perform_instructions(instructions)


###################
# Example 3
# Bank Question / Final Exam 2005
###################
def example3():
    instructions = [
        (1, Ops.PrRd),
        (2, Ops.PrWr, lambda _: 8),
        (3, Ops.PrRd),
        (1, Ops.PrRd),
        (2, Ops.PrWr, lambda x: 9),
    ]
    vi = VI(n_processors=len(set(x[0] for x in instructions)), memory_content=3)
    vi.perform_instructions(instructions)

###################
# Main
###################
# example1()
# example2()
# example3()
