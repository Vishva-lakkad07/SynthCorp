class ProductionSetup:
    def __init__(self):
        self.machines = []
        self.quality_rules = []
        self.assembly_config = {}
    
    def add_machine(self, machine):
        self.machines.append(machine)
    
    def add_quality_rule(self, rule):
        self.quality_rules.append(rule)
    
    def set_assembly_config(self, config):
        self.assembly_config = config

class ProductionBuilder:
    def __init__(self):
        self._setup = ProductionSetup()
    
    def add_machine(self, machine):
        self._setup.add_machine(machine)
        return self
    
    def add_quality_rule(self, rule):
        self._setup.add_quality_rule(rule)
        return self
    
    def set_assembly_config(self, config):
        self._setup.set_assembly_config(config)
        return self
    
    def build(self):
        return self._setup