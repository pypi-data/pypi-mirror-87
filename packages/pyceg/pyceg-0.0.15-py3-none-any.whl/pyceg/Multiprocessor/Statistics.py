class Statistics:
    def __init__(self):
        self.n_reads = 0
        self.n_writes = 0
        self.n_invalidations = 0
        self.n_state_changes = 0
        self.n_bus_latency = 0
        self.n_cache_misses = 0
        self.n_cache_to_cache_transfers = 0
        self.n_flushes = 0

    def info(self):
        stats = {
            "Reads": self.n_reads,
            "Writes": self.n_writes,
            "Invalidations": self.n_invalidations,
            "Bus Transactions": self.n_bus_latency,
            "States": self.n_state_changes,
            "Cache-to-Cache Transfers": self.n_cache_to_cache_transfers,
            "Cache Misses": self.n_cache_misses,
            "Flushes": self.n_flushes,
        }
        return stats
