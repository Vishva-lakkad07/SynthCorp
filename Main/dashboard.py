# import tkinter as tk
# from tkinter import ttk
# from states import MachineState

# class Dashboard:
#     def __init__(self, control_system):
#         self.control_system = control_system
#         self.root = tk.Tk()
#         self.root.title("SynthCorp Dashboard")
#         self.labels = {}
#         self.setup_gui()

#     def setup_gui(self):
#         self.notebook = ttk.Notebook(self.root)
#         self.notebook.pack(fill='both', expand=True)

#         self.tab_safety = ttk.Frame(self.notebook)
#         self.tab_assembling = ttk.Frame(self.notebook)
#         self.tab_production = ttk.Frame(self.notebook)
#         self.tab_inventory = ttk.Frame(self.notebook)

#         self.notebook.add(self.tab_safety, text="Safety")
#         self.notebook.add(self.tab_assembling, text="Assembling")
#         self.notebook.add(self.tab_production, text="Production")
#         self.notebook.add(self.tab_inventory, text="Inventory")

#         self._create_safety_controls()
#         self._register_safety_observer()
#         self._create_assembling_controls()
#         self._create_production_controls()
#         self._create_inventory_controls()

#     def _create_safety_controls(self):
#         frame = self.tab_safety

#         ttk.Label(frame, text="Emergency Shutdown for Machine", font=('Arial', 10)).pack(pady=5)
#         self.emergency_machine_var = tk.StringVar()
#         ttk.Combobox(frame, textvariable=self.emergency_machine_var,
#                      values=[m.name for m in self.control_system.machines],
#                      state='readonly').pack(pady=2)
#         ttk.Button(frame, text="Shutdown Selected Machine", command=self.emergency_shutdown).pack(pady=5)

#         ttk.Label(frame, text="Manual State Change", font=('Arial', 12, 'bold')).pack(pady=10)
#         self.machine_var = tk.StringVar()
#         ttk.Combobox(frame, textvariable=self.machine_var,
#                      values=[m.name for m in self.control_system.machines],
#                      state='readonly').pack(pady=2)

#         self.state_var = tk.StringVar()
#         ttk.Combobox(frame, textvariable=self.state_var,
#                      values=["Idle", "Active", "Maintenance", "Error"],
#                      state='readonly').pack(pady=2)
#         ttk.Button(frame, text="Set State", command=self._set_manual_state).pack(pady=5)

#         self.alert_box = tk.Text(frame, height=10)
#         self.alert_box.pack(fill='both', expand=True, padx=10, pady=5)

#     def _register_safety_observer(self):
#         class GUIObserver:
#             def __init__(self, text_widget):
#                 self.text_widget = text_widget
#             def message(self, msg):
#                 self.text_widget.insert('end', f"{msg}\n")
#                 self.text_widget.see('end')
        
#         gui_obs = GUIObserver(self.alert_box)
#         for m in self.control_system.machines:
#             if hasattr(m, 'register_obs'):
#                 m.register_obs(gui_obs)

#     def _create_assembling_controls(self):
#         frame = self.tab_assembling
#         ttk.Button(frame, text="Start Assembly", command=self.start_production).pack(pady=5)
#         ttk.Button(frame, text="Pause Assembly", command=self.pause_production).pack(pady=5)
        
#         for machine in self.control_system.machines:
#             label = ttk.Label(frame, text=f"{machine.name}: {machine.state.__class__.__name__}")
#             label.pack(anchor='w', padx=10, pady=2)
#             self.labels[machine.id] = label

#     def _create_production_controls(self):
#         frame = self.tab_production
#         ttk.Button(frame, text="Update Status", command=self.update_status).pack(pady=5)
#         for task in getattr(self.control_system._production_scheduler, 'tasks', []):
#             ttk.Label(frame, text=f"{task.name} (Priority: {task.priority}, Demand: {task.demand})").pack(anchor='w', padx=10)

#     def _create_inventory_controls(self):
#         frame = self.tab_inventory
#         ttk.Label(frame, text="Inventory Levels", font=('Arial', 12, 'bold')).pack(pady=5)
#         for material, qty in getattr(self.control_system.inventory_manager, 'stock', {}).items():
#             ttk.Label(frame, text=f"{material}: {qty}").pack(anchor='w', padx=10)

#     def _set_manual_state(self):
#         name = self.machine_var.get()
#         state = self.state_var.get()
#         if name and state:
#             for m in self.control_system.machines:
#                 if m.name == name:
#                     new_state = MachineState.get_state(state)
#                     m.set_state(new_state)
#                     if m.id in self.labels:
#                         self.labels[m.id].config(text=f"{m.name}: {state}State")
#                     break

#     def start_production(self):
#         if self.control_system._production_scheduler:
#             self.control_system._production_scheduler.schedule_production()

#     def pause_production(self):
#         if self.control_system._production_scheduler:
#             self.control_system._production_scheduler.pause_production()

#     def emergency_shutdown(self):
#         selected_name = self.emergency_machine_var.get()
#         if selected_name:
#             for machine in self.control_system.machines:
#                 if machine.name == selected_name:
#                     machine.set_state(MachineState.get_state("Error"))
#                     machine.emergency()
#                     print(f"[EMERGENCY] {machine.name} is now in Error state.")
#                     if machine.id in self.labels:
#                         self.labels[machine.id].config(text=f"{machine.name}: ErrorState")
#                     self.notebook.select(self.tab_assembling)
#                     break

#     def update_status(self):
#         for machine in self.control_system.machines:
#             if machine.id in self.labels:
#                 self.labels[machine.id].config(text=f"{machine.name}: {machine.state.__class__.__name__}")

#     def run(self):
#         self.root.mainloop()

# # from states import MachineState

# # class Dashboard:
# #     def __init__(self, control_system):
# #         self.control_system = control_system
# #         self.labels = {}
    
# #     def run(self):
# #         print("\n[Dashboard]")
# #         while True:
# #             print("\nDashboard Menu:")
# #             print("1. Show Machine Status")
# #             print("2. Start Production")
# #             print("3. Pause Production")
# #             print("4. Emergency Shutdown")
# #             print("5. Update Status")
# #             print("6. Show Inventory")
# #             print("7. Show Tasks")
# #             print("8. Exit Dashboard")
# #             option = input("Choose an option: ")

# #             if option == "1":
# #                 self.show_machine_status()
# #             elif option == "2":
# #                 self.start_production()
# #             elif option == "3":
# #                 self.pause_production()
# #             elif option == "4":
# #                 self.emergency_shutdown()
# #             elif option == "5":
# #                 self.update_status()
# #             elif option == "6":
# #                 self.control_system.inventory_manager.show_inventory()
# #             elif option == "7":
# #                 self.show_tasks()
# #             elif option == "8":
# #                 print("Exiting Dashboard.")
# #                 break
# #             else:
# #                 print("Invalid option.")

# #     def show_machine_status(self):
# #         print("\nMachine Status:")
# #         for machine in self.control_system.machines:
# #             print(f"{machine.name} (ID: {machine.id}): State - {machine.state.__class__.__name__}")

# #     def start_production(self):
# #         if self.control_system.production_scheduler:
# #             self.control_system.production_scheduler.schedule_production()

# #     def pause_production(self):
# #         if self.control_system.production_scheduler:
# #             self.control_system.production_scheduler.pause_production()

# #     def emergency_shutdown(self):
# #         selected_name = input("Enter machine name for emergency shutdown (or 'all' for all machines): ")
# #         if selected_name.lower() == 'all':
# #             for machine in self.control_system.machines:
# #                 machine.set_state(MachineState.get_state("Error"))
# #                 machine.emergency()
# #                 print(f"[EMERGENCY] {machine.name} is now in Error state.")
# #         else:
# #             for machine in self.control_system.machines:
# #                 if machine.name == selected_name:
# #                     machine.set_state(MachineState.get_state("Error"))
# #                     machine.emergency()
# #                     print(f"[EMERGENCY] {machine.name} is now in Error state.")
# #                     break
# #             else:
# #                 print("Machine not found.")

# #     def update_status(self):
# #         self.show_machine_status()

# #     def show_tasks(self):
# #         if self.control_system.production_scheduler:
# #             print("\nCurrent Tasks:")
# #             for task in self.control_system.production_scheduler.task_queue:
# #                 print(f"Task: {task.name}, Priority: {task.priority}, Demand: {task.demand}, Strategy: {task.strategy.__class__.__name__}")
# #         else:
# #             print("No scheduler available.")


from states import MachineState

class Dashboard:
    def __init__(self, control_system):
        self.control_system = control_system
        self.labels = {}
    
    def run(self):
        print("\n[Dashboard]")
        while True:
            print("\nDashboard Menu:")
            print("1. Show Machine Status")
            print("2. Start Production")
            print("3. Pause Production")
            print("4. Emergency Shutdown")
            print("5. Update Status")
            print("6. Show Inventory")
            print("7. Show Tasks")
            print("8. Exit Dashboard")
            option = input("Choose an option: ")

            if option == "1":
                self.show_machine_status()
            elif option == "2":
                self.start_production()
            elif option == "3":
                self.pause_production()
            elif option == "4":
                self.emergency_shutdown()
            elif option == "5":
                self.update_status()
            elif option == "6":
                self.control_system.inventory_manager.show_inventory()
            elif option == "7":
                self.show_tasks()
            elif option == "8":
                print("Exiting Dashboard.")
                break
            else:
                print("Invalid option.")

    def show_machine_status(self):
        print("\nMachine Status:")
        for machine in self.control_system.machines:
            print(f"{machine.name} (ID: {machine.id}): State - {machine.state.__class__.__name__}")

    def start_production(self):
        if self.control_system.production_scheduler:
            self.control_system.production_scheduler.schedule_production()

    def pause_production(self):
        if self.control_system.production_scheduler:
            self.control_system.production_scheduler.pause_production()

    def emergency_shutdown(self):
        selected_name = input("Enter machine name for emergency shutdown (or 'all' for all machines): ")
        if selected_name.lower() == 'all':
            for machine in self.control_system.machines:
                machine.set_state(MachineState.get_state("Error"))
                machine.emergency()
                print(f"[EMERGENCY] {machine.name} is now in Error state.")
        else:
            for machine in self.control_system.machines:
                if machine.name == selected_name:
                    machine.set_state(MachineState.get_state("Error"))
                    machine.emergency()
                    print(f"[EMERGENCY] {machine.name} is now in Error state.")
                    break
            else:
                print("Machine not found.")

    def update_status(self):
        self.show_machine_status()

    def show_tasks(self):
        if self.control_system.production_scheduler:
            print("\nCurrent Tasks:")
            for task in self.control_system.production_scheduler.task_queue:
                print(f"Task: {task.name}, Priority: {task.priority}, Demand: {task.demand}, Strategy: {task.strategy.__class__.__name__}")
        else:
            print("No scheduler available.")