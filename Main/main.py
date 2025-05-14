from central_control import CentralControlSystem
from machine import Machine, AssemblyRobot, PackagingRobot, QualityControlBot
from machine_factory import MachineFactory
from adapter import LegacyMachine, LegacyMachineAdapter
from observer import Engineer, Technician, ErrorRecovery
from task import Task
from production_strategy import ProductionStrategy, MassProductionStrategy, CustomBatchProductionStrategy, OnDemandProductionStrategy
from inventory_management import InventoryManager
from safety_manager import SafetyManager
from production_scheduler import ProductionScheduler
from decorator import ErrorDetectionDecorator, EnergyEfficientDecorator
from states import MachineState
from command_invoker import CommandInvoker
from Assembly_command import MoveCommand, AssembleCommand
from dashboard import Dashboard  # Import the new dashboard.py

def decorate_machine(machine):
    """Helper function to apply decorators based on machine type"""
    try:
        if isinstance(machine, AssemblyRobot):
            return ErrorDetectionDecorator(machine)
        if hasattr(machine, 'name') and isinstance(machine.name, str):
            if "Cutting" in machine.name or "Drilling" in machine.name or "Welding" in machine.name:
                return EnergyEfficientDecorator(machine)
        return machine
    except Exception as e:
        print(f"Error applying decorator: {e}")
        return machine

def create_machine(choice, id, name):
    """Factory method to create machines"""
    try:
        if choice == "1":
            return AssemblyRobot(id, name)
        elif choice == "2":
            return PackagingRobot(id, name)
        elif choice == "3":
            return QualityControlBot(id, name)
        elif choice == "4":
            return MachineFactory.create_machine("Cutting", id, name)
        elif choice == "5":
            return LegacyMachineAdapter(id, name, LegacyMachine())
        return None
    except Exception as e:
        print(f"Error creating machine: {e}")
        return None

def main():
    # Initialize control system and managers
    try:
        control_system = CentralControlSystem()
        inventory_manager = InventoryManager()
        safety_manager = SafetyManager()
        scheduler = ProductionScheduler()
        
        control_system.set_inventory_manager(inventory_manager)
        control_system.set_safety_manager(safety_manager)
        control_system.set_production_scheduler(scheduler)
        
        inventory_manager.add_resource("steel", 1000, 100)
        inventory_manager.add_resource("plastic", 500, 50)
        # inventory_manager.add_observer(OrderingSystem())

        # Check inventory at startup
        print("\n[System Startup Inventory Check]")
        inventory_manager.check_inventory()
        inventory_manager.show_inventory()
    except Exception as e:
        print(f"Error initializing system: {e}")
        return

        # Check inventory at startup
        print("\n[System Startup Inventory Check]")
        inventory_manager.check_inventory()
        inventory_manager.show_inventory()
    except Exception as e:
        print(f"Error initializing system: {e}")
        return

    # Initialize observers
    try:
        engineer = Engineer("John")
        technician = Technician("Alice")
        recovery = ErrorRecovery()
    except Exception as e:
        print(f"Error initializing observers: {e}")
        return

    # Command invoker for testing Assembly_command
    invoker = CommandInvoker()

    def create_new_machine():
        print("\n[Machine Creation]")
        print("1. Assembly Robot\n2. Packaging Robot\n3. Quality Control Bot")
        print("4. Cutting Machine\n5. Legacy Machine")
        choice = input("Choose machine type: ")
        id = input("Enter Machine ID: ")
        name = input("Enter Machine Name: ")

        machine = create_machine(choice, id, name)
        if not machine:
            print("Invalid choice or error creating machine.")
            return

        # Apply decorators if needed
        decorate = input("Apply decorator? (1. Error Detection, 2. Energy Efficient, n for none): ")
        if decorate == "1":
            machine = ErrorDetectionDecorator(machine)
        elif decorate == "2":
            machine = EnergyEfficientDecorator(machine)

        # Add observers and register machine
        try:
            machine.attach_observer(engineer)
            machine.attach_observer(technician)
            machine.attach_observer(recovery)
            control_system.add_machine(machine)
            scheduler.add_machine(machine)  # Add to scheduler for production
            print(f"{name} created and added successfully.")
        except Exception as e:
            print(f"Error registering machine: {e}")

    def create_new_task():
        print("\n[Task Creation]")
        try:
            name = input("Task name: ")
            priority = int(input("Priority (1=high): "))
            demand = int(input("Demand: "))
            print("Strategy:\n1. Mass Production\n2. Custom Batch\n3. On-Demand")
            strat = input("Choose strategy: ")
            
            if strat == "1":
                strategy = MassProductionStrategy()
            elif strat == "2":
                batch_size = int(input("Enter batch size: "))
                strategy = CustomBatchProductionStrategy(batch_size)
            elif strat == "3":
                strategy = OnDemandProductionStrategy()
            else:
                print("Invalid strategy.")
                return

            task = Task(name, priority, demand, strategy)
            scheduler.add_task(task)
            print(f"Task '{name}' added successfully.")
        except ValueError:
            print("Invalid input. Priority, demand, and batch size must be numbers.")
        except Exception as e:
            print(f"Error creating task: {e}")

    def test_assembly_commands():
        if not control_system.machines:
            print("No machines available. Create a machine first.")
            return
        machine_id = input("Enter Machine ID to test assembly commands: ")
        machine = control_system.get_machine(machine_id)
        if machine:
            print(f"Testing assembly commands on {machine.name}")
            invoker.execute_command(MoveCommand(machine))
            invoker.execute_command(AssembleCommand(machine))
            invoker.undo_last_command()
        else:
            print("Machine not found.")

    while True:
        print("\n===== Smart Factory Control Menu =====")
        print("1. Create Machine")
        print("2. Create Task")
        print("3. Consume Inventory Material")
        print("4. Simulate Error")
        print("5. Schedule Production")
        # print("6. Undo Last Schedule")
        # print("7. Dynamic Reschedule")
        print("6. Open Dashboard")
        print("7. Show Inventory")
        print("8. Test Assembly Commands")
        print("9. Exit")

        option = input("Enter your choice: ")

        if option == "1":
            create_new_machine()
        elif option == "2":
            create_new_task()
        elif option == "3":
            mat = input("Material name: ")
            try:
                qty = int(input("Quantity to consume: "))
                inventory_manager.consume_material(mat, qty)
            except ValueError:
                print("Invalid quantity. Must be a number.")
            except Exception as e:
                print(f"Error consuming material: {e}")
        elif option == "4":
            if control_system.machines:
                machine_id = input("Enter Machine ID to simulate error: ")
                try:
                    machine = control_system.get_machine(machine_id)
                    if machine:
                        machine.set_state(MachineState.get_state("Error"))
                        safety_manager.check_safety(machine)
                    else:
                        print("Machine not found.")
                except Exception as e:
                    print(f"Error simulating error: {e}")
            else:
                print("No machines available.")
        elif option == "5":
            try:
                scheduler.schedule_production()
            except Exception as e:
                print(f"Error scheduling production: {e}")
        # elif option == "6":
        #     try:
        #         scheduler.undo_last_action()
        #     except Exception as e:
        #         print(f"Error undoing last action: {e}")
        # elif option == "7":
        #     try:
        #         scheduler.dynamic_reschedule()
        #     except Exception as e:
        #         print(f"Error during dynamic rescheduling: {e}")
        elif option == "6":
            try:
                dashboard = Dashboard(control_system)
                dashboard.run()
            except Exception as e:
                print(f"Error running dashboard: {e}")
        elif option == "7":
            try:
                inventory_manager.show_inventory()
            except Exception as e:
                print(f"Error showing inventory: {e}")
        elif option == "8":
            test_assembly_commands()
        elif option == "9":
            print("Exiting Smart Factory Control.")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()