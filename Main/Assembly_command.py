class Command:
    def execute(self):
        raise NotImplementedError

    def undo(self):
        raise NotImplementedError
    
class MoveCommand(Command):
    def __init__(self, machine):
        self.machine = machine

    def execute(self):
        self.machine.move()

    def undo(self):
        print(f"Undo move for {self.machine.__class__.__name__}")

class AssembleCommand(Command):
    def __init__(self, machine):
        self.machine = machine

    def execute(self):
        self.machine.assemble()

    def undo(self):
        print(f"Undo assemble for {self.machine.__class__.__name__}")
