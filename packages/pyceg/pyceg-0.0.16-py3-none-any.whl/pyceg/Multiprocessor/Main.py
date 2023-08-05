from MSI import MSI
from MESI import MESI
from Operations import MSIOps as Ops
from CacheCoherence import protocols


###################
# Example 1
# Quiz 13 2020
###################
def example1():
    """
    Read Latency MSI < MESI? True because MSI has lesser activities
    """
    instructions = [
        (2, Ops.PrRd),
        (1, Ops.PrRd),
    ]
    msi = MSI(n_processors=2, memory_content=0)
    msi.perform_instructions(instructions)

    mesi = MESI(n_processors=2, memory_content=0)
    mesi.perform_instructions(instructions)


###################
# Example 2
# Quiz 13 2020
###################
def example2():
    """
    Write Latency MSI < MESI? False because 2nd row in MESI has no transactions
    """
    instructions = [
        (1, Ops.PrRd),
        (1, Ops.PrWr, lambda x: x),
    ]
    msi = MSI(n_processors=2, memory_content=0)
    msi.perform_instructions(instructions)

    mesi = MESI(n_processors=2, memory_content=0)
    mesi.perform_instructions(instructions)


###########################
# Example 3
# Nov 6th 2020 Zoom Lecture
##########################
def example3():
    instructions = [
        (1, Ops.PrRd),
        (2, Ops.PrRd),
        (2, Ops.PrWr, lambda x: 10),
        (2, Ops.PrRd),
        (2, Ops.PrWr, lambda x: 15),
        (1, Ops.PrWr, lambda x: 20),
        (2, Ops.PrRd),
    ]
    msi = MSI(n_processors=2, memory_content=5)
    msi.perform_instructions(instructions)


###################
# Example 4
# DGD 5 Fall 2020 and Quiz 2 2019
# Question 3
###################
def example4():
    instructions = [
        (1, Ops.PrRd),
        (2, Ops.PrRd),
        (2, Ops.PrWr, lambda x: x + 2),
        (1, Ops.PrWr, lambda x: x * 2),
        (2, Ops.PrRd),
    ]
    msi = MSI(n_processors=2, memory_content=10)
    msi.perform_instructions(instructions)

    # msi = MSI(n_processors=2, memory_content=10)
    # msi.perform_instructions(instructions)


###################
# Example 5
# DGD 5 Fall 2020 and Quiz 2 2019
# Question 3
###################
def example5():
    instructions = [
        (2, Ops.PrRd),
        (1, Ops.PrWr, lambda x: x),
        (1, Ops.PrWr, lambda x: x),
        (2, Ops.PrRd),
    ]
    mesi = MESI(n_processors=2, memory_content=0)
    # This initial state was given in the question Processor 1: E
    mesi.set_processor_state(1, "E")
    mesi.perform_instructions(instructions)


###################
# Example 6
# Bank Question / Final Exam 2005
###################
def example6():
    instructions = [
        (1, Ops.PrRd),
        (2, Ops.PrWr, lambda x: 8),
        (3, Ops.PrRd),
        (1, Ops.PrRd),
        (2, Ops.PrWr, lambda x: 9),
    ]
    msi = MSI(n_processors=3, memory_content=3)
    msi.perform_instructions(instructions)


###################
# Multiple Protocols Load Testing
###################
def example7():
    instructions = [
        (1, Ops.PrRd),
        (3, Ops.PrRd),
        (3, Ops.PrWr, lambda x: x + 2),
        (1, Ops.PrRd),
        (2, Ops.PrRd),
        (2, Ops.PrWr, lambda x: x + 2),
    ]
    for name, protocol in protocols.items():
        p = protocol(n_processors=3, memory_content=3)
        p.perform_instructions(instructions, display=False)
        print(p.statistics())

###################
# Main
###################
# example1()
# example2()
# example3()
# example4()
# example5()
# example6()
# example7()
