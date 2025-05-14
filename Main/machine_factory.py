from machine import Machine

class CuttingMachine(Machine):
    def perform_action(self):
        self._state.perform_action(self)
        print(f"{self.name} cutting materials")

class DrillingMachine(Machine):
    def perform_action(self):
        self._state.perform_action(self)
        print(f"{self.name} drilling parts")

class WeldingMachine(Machine):
    def perform_action(self):
        self._state.perform_action(self)
        print(f"{self.name} welding components")

class MachineFactory:
    @staticmethod
    def create_machine(machine_type, id, name):
        if machine_type == "Cutting":
            return CuttingMachine(id, name)
        elif machine_type == "Drilling":
            return DrillingMachine(id, name)
        elif machine_type == "Welding":
            return WeldingMachine(id, name)
        else:
            raise ValueError(f"Unknown machine type: {machine_type}")