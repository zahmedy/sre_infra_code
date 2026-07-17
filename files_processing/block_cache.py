from collections import OrderedDict
import threading

class ConcurrentBlockCache:
    def __init__(self, total_capacity: int, num_shards: int = 16):
        self.num_shards = num_shards

        shard_capacity = max(1, total_capacity // num_shards)

        self.shards = [BlockCache(shard_capacity) for _ in range(num_shards)]
        self.locks = [threading.Lock() for _ in range(num_shards)]

    def _get_shard_index(self, block_id: int) -> int:
        return block_id % self.num_shards
    
    def read_block(self, block_id: int) -> str:
        idx = self._get_shard_index(block_id)

        # Lock per shard
        with self.locks[idx]:
            return self.shards[idx].read_block(block_id)
    
    def write_block(self, block_id: int, data: str) -> None:
        idx = self._get_shard_index(block_id)

        with self.locks[idx]:
            self.shards[idx].write_block(block_id, data)


class BlockCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()

    def _ensure_capacity(self) -> None:
        # Check if we still have space 
        if len(self.cache) >= self.capacity:
            # LRU block need to be ejected
            lru_block_id, block_metdata = self.cache.popitem(last=False)
            if block_metdata["dirty"]:
                self._flush_to_disk(lru_block_id, block_metdata["data"])
            

    def read_block(self, block_id: int) -> str:
        """ Returns the block data. Simulates disk read on miss. """
        # Check if block in cache first
        if block_id in self.cache:
            self.cache.move_to_end(block_id, last=True)
            return self.cache[block_id]["data"]

        # Cache Miss
        print(f"[DISK] Fetching block {block_id}")
        data = f"data for block {block_id}" # Simulate data from disk

        self.cache[block_id] = {
            "data": data,
            "dirt": False     # Fresh from disk is not dirty, yet!
        }
        # Mark block as most used
        self.cache.move_to_end(block_id, last=True)

        self._ensure_capacity()
        return data

    def write_block(self, block_id: int, data: str) -> None:
        """ Updates cache and marks block as dirty. """
        self.cache[block_id] = {
            "data": data,
            "dirty": True   # Since we writting to RAM it still dirty
        }
        
        self.cache.move_to_end(block_id, last=True)

        self._ensure_capacity()

    def _flush_to_disk(self, block_id: int, data: str) -> None:
        """ Simulates writing a dirty block back to the physical block device """
        print(f"[DISK] Persisting dirty block {block_id}")