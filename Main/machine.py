from abc import ABC, abstractmethod
from states import MachineState

class Machine(ABC):
    def __init__(self, id, name):
        self._id = id
        self._name = name
        self._state = MachineState.get_state("Idle")
        self._state_history = []
        self._production_strategy = None
        self._observers = []
    
    @property
    def id(self):
        return self._id
    
    @property
    def name(self):
        return self._name
    
    @property
    def state(self):
        return self._state
    
    def set_state(self, state):
        self._state = state
        self._state_history.append(state)
        print(f"{self.name} state changed to {state.__class__.__name__}")
        self.notify_observers()
    
    def set_production_strategy(self, strategy):
        self._production_strategy = strategy
        print(f"{self.name} set production strategy to {strategy.__class__.__name__}")
    
    def execute_production(self):
        if self._production_strategy:
            self._production_strategy.execute(self)
        else:
            print(f"{self.name} has no production strategy set")
    
    def attach_observer(self, observer):
        self._observers.append(observer)
    
    def detach_observer(self, observer):
        self._observers.remove(observer)
    
    def notify_observers(self):
        for observer in self._observers:
            observer.update(self)
    
    @abstractmethod
    def perform_action(self):
        pass

    def emergency(self):
        self.set_state(MachineState.get_state("Error"))

    def move(self):  # Added for MoveCommand
        print(f"{self.name} moving to position")

    def assemble(self):  # Added for AssembleCommand
        print(f"{self.name} assembling components")

class AssemblyRobot(Machine):
    def perform_action(self):
        self._state.perform_action(self)
        print(f"{self.name} assembling parts")

class PackagingRobot(Machine):
    def perform_action(self):
        self._state.perform_action(self)
        print(f"{self.name} packaging products")

class QualityControlBot(Machine):
    def perform_action(self):
        self._state.perform_action(self)
        print(f"{self.name} inspecting products")