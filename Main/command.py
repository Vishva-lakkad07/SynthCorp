from abc import ABC, abstractmethod
from states import MachineState

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass
    
    @abstractmethod
    def undo(self):
        pass

class StartProductionCommand(Command):
    def __init__(self, machine, task):
        self.machine = machine
        self.task = task
    
    def execute(self):
        if self.machine.state.__class__.__name__ != "Idle":
            print(f"Cannot start production on {self.machine.name}: not idle")
            return
        print(f"Starting production on {self.machine.name}")
        self.machine.set_production_strategy(self.task.strategy)
        self.machine.execute_production()
    
    def undo(self):
        print(f"Undoing production start on {self.machine.name}")
        self.machine.set_state(MachineState.get_state("Idle"))
        self.machine.perform_action()

class PauseProductionCommand(Command):
    def __init__(self, machine):
        self.machine = machine
        self.previous_state = None
    
    def execute(self):
        if self.machine.state.__class__.__name__ != "Active":
            print(f"Cannot pause production on {self.machine.name}: not active")
            return
        print(f"Pausing production on {self.machine.name}")
        self.previous_state = self.machine.state
        self.machine.set_state(MachineState.get_state("Idle"))
        self.machine.perform_action()
    
    def undo(self):
        print(f"Resuming production on {self.machine.name}")
        if self.previous_state:
            self.machine.set_state(self.previous_state)
            self.machine.perform_action()

class EmergencyShutdownCommand(Command):
    def __init__(self, machine):
        self.machine = machine
    
    def execute(self):
        print(f"Emergency shutdown on {self.machine.name}")
        self.machine.set_state(MachineState.get_state("Error"))
        self.machine.perform_action()
    
    def undo(self):
        print(f"Undoing emergency shutdown on {self.machine.name}")
        self.machine.set_state(MachineState.get_state("Idle"))
        self.machine.perform_action()

class RescheduleCommand(Command):
    def __init__(self, scheduler, task):
        self.scheduler = scheduler
        self.task = task
    
    def execute(self):
        print(f"Rescheduling task {self.task.name}")
        self.scheduler.task_queue.append(self.task)
        self.scheduler.dynamic_reschedule()
    
    def undo(self):
        print(f"Undoing reschedule of task {self.task.name}")
        if self.task in self.scheduler.task_queue:
            self.scheduler.task_queue.remove(self.task)