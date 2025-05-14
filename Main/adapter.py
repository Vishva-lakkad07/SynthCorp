from machine import Machine 

class LegacyMachine:
    def old_operation(self):
        print("Legacy machine performing old operation")

class LegacyMachineAdapter(Machine):
    def __init__(self, id, name, legacy_machine):
        super().__init__(id, name)
        self.legacy_machine = legacy_machine
    
    def perform_action(self):
        self._state.perform_action(self)
        self.legacy_machine.old_operation()