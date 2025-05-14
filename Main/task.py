import time

class Task:
    def __init__(self, name, priority, demand, strategy, urgent=False):
        self.name = name
        self.priority = priority
        self.demand = demand
        self.strategy = strategy
        self.deadline = time.time() + 86400  
        self.completed = False
        self.urgent = urgent