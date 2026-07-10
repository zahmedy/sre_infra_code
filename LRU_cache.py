class Node:
    def __init__(self, key: str, value: str) -> None:
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}

        self.head = Node("", "")  # LRU side
        self.tail = Node("", "")  # MRU side

        self.head.next = self.tail
        self.tail.prev = self.head

    def remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def add_mru(self, node):
        previous = self.tail.prev

        previous.next = node
        node.prev = previous
        node.next = self.tail
        self.tail.prev = node


    def get(self, key: str) -> str | None:
        if key not in self.cache:
            return None
        
        node = self.cache[key]
        self.remove(node)
        self.add_mru(node)

        return self.cache[key].value

    def put(self, key: str, value: str) -> None:
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self.remove(node)
            self.add_mru(node)
            return
        
        node = Node(key, value)
        self.cache[key] = node
        self.add_mru(node)

        if len(self.cache) > self.capacity:
            lru = self.head.next
            self.remove(lru)
            del self.cache[lru.key]
