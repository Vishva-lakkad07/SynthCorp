class CentralControlSystem:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CentralControlSystem, cls).__new__(cls)
            cls._instance.machines = []
            cls._instance.inventory_manager = None
            cls._instance.safety_manager = None
            cls._instance.production_scheduler = None
        return cls._instance
    
    def add_machine(self, machine):
        self.machines.append(machine)
    
    def get_machine(self, machine_id):
        for machine in self.machines:
            if machine.id == machine_id:
                return machine
        return None
    
    def set_inventory_manager(self, manager):
        self.inventory_manager = manager
    
    def set_safety_manager(self, manager):
        self.safety_manager = manager
    
    def set_production_scheduler(self, scheduler):
        self.production_scheduler = scheduler