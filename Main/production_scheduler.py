from production_strategy import ProductionStrategy
from command import StartProductionCommand, PauseProductionCommand, RescheduleCommand
from states import MachineState
import time

class ProductionScheduler:
    def __init__(self):
        self.machines = []
        self.task_queue = []
        self.command_history = []
    
    def add_machine(self, machine):
        self.machines.append(machine)
    
    def add_task(self, task):
        task.deadline = getattr(task, 'deadline', time.time() + 86400)
        task.completed = getattr(task, 'completed', False)
        self.task_queue.append(task)
        task.strategy.add_task(task)
        print(f"Task added: {task.name}, Deadline: {task.deadline}, Current Time: {time.time()}")
    
    def schedule_production(self):
        print(f"Task Queue: {[task.name for task in self.task_queue]}")
        print(f"Machines: {[machine.name for machine in self.machines]}")
        for task in self.task_queue[:]:
            print(f"Checking task: {task.name}, Completed: {task.completed}, Expired: {self.is_task_expired(task)}")
            if task.completed or self.is_task_expired(task):
                self.task_queue.remove(task)
                print(f"Task {task.name} removed from queue (completed or expired)")
                continue
            for machine in self.machines:
                if machine.state.__class__.__name__ == "Idle":
                    if task.strategy.is_compatible(task, machine):
                        command = StartProductionCommand(machine, task)
                        command.execute()
                        if machine.state.__class__.__name__ == "Active":
                            self.task_queue.remove(task)
                            self.command_history.append(command)
                            print(f"Task {task.name} scheduled on {machine.name}")
                        else:
                            print(f"Failed to execute task {task.name} on {machine.name}")
                        break
    
    def pause_production(self):
        for machine in self.machines:
            if machine.state.__class__.__name__ == "Active":
                command = PauseProductionCommand(machine)
                command.execute()
                self.command_history.append(command)
    
    def undo_last_action(self):
        if self.command_history:
            command = self.command_history.pop()
            command.undo()
            # Re-add task to queue if it's a StartProductionCommand
            if isinstance(command, StartProductionCommand):
                task = command.task
                task.completed = False  # Reset completed status
                self.task_queue.append(task)
                print(f"Task {task.name} re-added to queue for rescheduling")
        else:
            print("No actions to undo.")
    
    def dynamic_reschedule(self):
        idle_machines = [m for m in self.machines if m.state.__class__.__name__ == "Idle"]
        if idle_machines and self.task_queue:
            print("Dynamically rescheduling tasks...")
            self.rebalance_priorities()
            self.schedule_production()
        else:
            print("No idle machines or tasks to reschedule.")
    
    def rebalance_priorities(self):
        current_time = time.time()
        for task in self.task_queue:
            if hasattr(task, 'deadline') and task.deadline < current_time + 600:
                task.priority += 2
            if hasattr(task, 'urgent') and task.urgent:
                task.priority += 1
    
    def is_task_expired(self, task):
        if hasattr(task, 'deadline'):
            return time.time() > task.deadline
        return False
    
    def handle_machine_failure(self, machine):
        for task in self.task_queue[:]:
            if task.strategy.is_compatible(task, machine):
                command = RescheduleCommand(self, task)
                command.execute()
                self.command_history.append(command)