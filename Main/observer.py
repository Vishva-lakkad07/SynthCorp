from abc import ABC, abstractmethod
from command_invoker import CommandInvoker
from Assembly_command import MoveCommand, AssembleCommand
from machine_factory import MachineFactory
from states import MachineState

class Observer(ABC):
    @abstractmethod
    def update(self, machine):
        pass

class Engineer(Observer):
    def __init__(self, name):
        self.name = name
    
    def update(self, machine):
        if machine.state.__class__.__name__ in ["Error", "Maintenance"]:
            print(f"Engineer {self.name} notified: {machine.name} is in {machine.state.__class__.__name__} state")

class Technician(Observer):
    def __init__(self, name):
        self.name = name
    
    def update(self, machine):
        if machine.state.__class__.__name__ == "Error":
            print(f"Technician {self.name} notified: {machine.name} is in Error state. Beginning diagnostic...")
            print(f"Technician {self.name} completed diagnostics for {machine.name}.")

class ErrorRecovery(Observer):
    def __init__(self):
        self.invoker = CommandInvoker()
        factory = MachineFactory()
        self.repair_machines = {
            "Cutting": factory.create_machine("Cutting", "RC1", "CuttingRepairMachine"),
            "Drilling": factory.create_machine("Drilling", "RD1", "DrillingRepairMachine"),
            "Welding": factory.create_machine("Welding", "RW1", "WeldingRepairMachine")
        }

    def update(self, machine):
        if machine.state.__class__.__name__ == "Error":
            print(f"ErrorRecovery: Repairing {machine.name} using repair sequence...")
            for tool_type, tool in self.repair_machines.items():
                self.invoker.execute_command(MoveCommand(tool))
                self.invoker.execute_command(AssembleCommand(tool))
            idle = MachineState.get_state("Idle")
            machine.set_state(idle)
            print(f"ErrorRecovery: {machine.name} state set to Idle after repair.")
