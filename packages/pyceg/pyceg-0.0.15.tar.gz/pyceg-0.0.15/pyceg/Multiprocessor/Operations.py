###################
# Operations
###################


class VIOps:
    # Processor
    PrRd = "PrRd"  # Processor Read
    PrWr = "PrWr"  # Processor Write
    PrInv = "PrInv"  # Processor Invalidate

    # Bus
    BusRd = "BusRd"  # Read Request for a block
    BusRdX = "BusRdX"  # Write a word to memory and invalidate other copies
    BusWr = "BusWr"


class MSIOps:
    # Processor
    PrRd = "PrRd"  # Processor Read
    PrWr = "PrWr"  # Processor Write
    PrInv = "PrInv"  # Processor Invalidate

    # Bus
    BusRd = "BusRd"  # Read Request for a block
    BusRdX = "BusRdX"  # Write a word to memory and invalidate other copies
    BusUpgr = "BusUpgr"  # Invalidate Other copies
    BusUpdate = "BusUpdate"  # Update Other copies
    Flush = "Flush"  # Supply a block to requesting cache


class MESIOps:
    # Processor
    PrRd = "PrRd"  # Processor Read
    PrWr = "PrWr"  # Processor Write
    PrInv = "PrInv"  # Processor Invalidate

    # Bus
    BusRd = "BusRd"  # Read Request for a block
    BusRdX = "BusRdX"  # Write a word to memory and invalidate other copies
    BusUpgr = "BusUpgr"  # Invalidate Other copies
    BusUpdate = "BusUpdate"  # Update Other copies
    Flush = "Flush"  # Supply a block to requesting cache
