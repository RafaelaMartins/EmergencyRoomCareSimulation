from heapq import heappop, heappush

class Queue():

    def __init__(self, priority=False):
        
        self.priority = priority
        self.queue = []
        self.time = [] # guarda tempo em fila de cada paciente que entra nessa fila
        self.size = [] # guarda tamanho da fila toda vez que alguém entra ou

    @property
    def empty(self):
        return len(self.queue) == 0

    def insert(self, element, count=0):
        
        try:
            priority = element.time
        except Exception as e:
            priority = element.priority

        if self.priority:
            self.add_priority_queue(priority, count, element)
        else:
            self.queue.append(element)

    def next(self):
        if self.priority:
            return heappop(self.queue)[-1]
        else:    
            return self.queue.pop()

    def add_priority_queue(self, priority, count, entry):
        entry = [priority, count, entry]
        heappush(self.queue, entry)

    def save_size(self):
        self.size.append(len(self.queue))
        
