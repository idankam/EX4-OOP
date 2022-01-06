import sys
class PriorityQueue:
    def __init__(self):
        self.queue = []

    def __str__(self):
        return ' '.join([str(i) for i in self.queue])

    # for checking if the queue is empty
    def isEmpty(self):
        return len(self.queue) == 0

    # for inserting an element in the queue
    def insert(self, data):
        self.queue.append(data)
    def size(self):
        return len(self.queue)

    def delete(self):
        try:
            min = len(self.queue) -1
            for i in range(len(self.queue)):
                if self.queue[i].weight < self.queue[min].weight:
                    min = i
            item = self.queue[min]
            del self.queue[min]
            return item
        except IndexError:
            print()
            exit()