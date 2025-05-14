from command import EmergencyShutdownCommand 
from central_control import CentralControlSystem

class SafetyManager:
    def __init__(self):
        self.control_system = CentralControlSystem()
    
    def check_safety(self, machine):
        if machine.state.__class__.__name__ == "Error":
            print(f"Safety violation detected on {machine.name}")
            self.emergency_shutdown()
    
    def emergency_shutdown(self):
        for machine in self.control_system.machines:
            command = EmergencyShutdownCommand(machine)
            command.execute()