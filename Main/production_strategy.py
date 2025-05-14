from abc import ABC, abstractmethod
from states import MachineState

class ProductionStrategy(ABC):
    def __init__(self, tasks=None):
        self.tasks = tasks or []
    
    def add_task(self, task):
        self.tasks.append(task)
    
    def get_highest_priority_task(self):
        if not self.tasks:
            return None
        return sorted(self.tasks, key=lambda x: (-x.priority, -x.demand))[0]
    
    def is_compatible(self, task, machine):
        return machine.state.__class__.__name__ == "Idle"  # Basic check; enhance if needed
    
    @abstractmethod
    def execute(self, machine):
        pass

class MassProductionStrategy(ProductionStrategy):
    def execute(self, machine):
        task = self.get_highest_priority_task()
        if not task:
            print(f"{machine.name} no tasks available for Mass Production")
            return
        print(f"{machine.name} executing Mass Production: producing 1000 units, task: {task.name}, priority: {task.priority}, demand: {task.demand}")
        machine.set_state(MachineState.get_state("Active"))
        machine.perform_action()
        task.completed = True

class CustomBatchProductionStrategy(ProductionStrategy):
    def __init__(self, batch_size, tasks=None):
        super().__init__(tasks)
        self.batch_size = batch_size
    
    def execute(self, machine):
        task = self.get_highest_priority_task()
        if not task:
            print(f"{machine.name} no tasks available for Custom Batch")
            return
        print(f"{machine.name} executing Custom Batch: producing {self.batch_size} units, task: {task.name}, priority: {task.priority}, demand: {task.demand}")
        machine.set_state(MachineState.get_state("Active"))
        machine.perform_action()
        task.completed = True

class OnDemandProductionStrategy(ProductionStrategy):
    def execute(self, machine):
        task = self.get_highest_priority_task()
        if not task:
            print(f"{machine.name} no tasks available for On-Demand")
            return
        print(f"{machine.name} executing On-Demand: task: {task.name}, priority: {task.priority}, demand: {task.demand}")
        machine.set_state(MachineState.get_state("Active"))
        machine.perform_action()
        task.completed = True