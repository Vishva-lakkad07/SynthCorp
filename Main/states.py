from abc import ABC, abstractmethod

class MachineState(ABC):
    _states = {}

    @classmethod
    def get_state(cls, state_name):
        if state_name not in cls._states:
            if state_name == "Idle":
                cls._states[state_name] = IdleState()
            elif state_name == "Active":
                cls._states[state_name] = ActiveState()
            elif state_name == "Maintenance":
                cls._states[state_name] = MaintenanceState()
            elif state_name == "Error":
                cls._states[state_name] = ErrorState()
        return cls._states[state_name]
    
    @abstractmethod
    def perform_action(self, machine):
        pass

class IdleState(MachineState):
    def perform_action(self, machine):
        print(f"{machine.name} is idle, ready for task")

class ActiveState(MachineState):
    def perform_action(self, machine):
        print(f"{machine.name} is actively producing")

class MaintenanceState(MachineState):
    def perform_action(self, machine):
        print(f"{machine.name} is under maintenance")

class ErrorState(MachineState):
    def perform_action(self, machine):
        print(f"{machine.name} is in error state, requires attention")