class SimpleAllocator:

    def __init__(self, size: int):
        self.free_list = list(reversed(range(size)))
        self.allocated = []

    def alloc(self):
        if len(self.free_list) > 0:
            e = self.free_list.pop()
            self.allocated.append(e)
            return e
        else:
            raise MemoryError("Not enough memory")

    def free(self, e: int):
        self.allocated.remove(e)
        self.free_list.append(e)
