from abc import ABC
from machine import Machine

class MachineDecorator(Machine, ABC):
    def __init__(self, machine):
        self._machine = machine
        super().__init__(machine.id, machine.name)
        self._state = machine.state
        self._observers = machine._observers
    
    def set_state(self, state):
        self._machine.set_state(state)
    
    def perform_action(self):
        self._machine.perform_action()

    def emergency(self):
        self._machine.emergency()

    def set_production_strategy(self, strategy):
        self._machine.set_production_strategy(strategy)

    def execute_production(self):
        self._machine.execute_production()

    def attach_observer(self, observer):
        self._machine.attach_observer(observer)

    def notify_observers(self):
        self._machine.notify_observers()

class ErrorDetectionDecorator(MachineDecorator):
    def perform_action(self):
        print(f"Checking for errors on {self.name}")
        super().perform_action()

class EnergyEfficientDecorator(MachineDecorator):
    def perform_action(self):
        print(f"Optimizing energy usage on {self.name}")
        super().perform_action()
        self._machine.emergency()