📌 Project Overview
SynthCorp is a smart and automated manufacturing system built using Object-Oriented Programming and Design Patterns. It simulates an AI-driven production plant featuring robotic machines, real-time inventory tracking, and optimized workflows. The system recovers from a major software failure and restores efficiency, safety, and control using advanced programming concepts.

🔧 Key Features
OOP Concepts: Encapsulation, Inheritance, Polymorphism, Abstraction.
Machine Types: AssemblyRobot, PackagingRobot, QualityControlBot.
Production Modes: Mass, Custom Batch, On-Demand.

🧱 Design Patterns
🏗️ Creational Patterns
Factory: Creates machine types like CuttingMachine, WeldingMachine, etc.
Singleton: CentralControlSystem ensures one global instance managing the production workflow.
Builder: Configures custom assembly lines and defines quality check rules.

🧱 Structural Patterns
Facade: Provides a unified dashboard for monitoring and controlling systems.
Adapter: Integrates legacy machines with the new smart control system.
Decorator: Dynamically adds features like EnergySaving mode or FaultDetection to machines.

🔁 Behavioral Patterns
Observer: Notifies engineers of malfunctions or when machines need maintenance.
Strategy: Switches between scheduling strategies like PriorityBased and DemandDriven.
Command: Supports undo/redo for production actions like pause, cancel, and machine commands like Move and Assemble.
State: Tracks machine states such as Idle, Active, Maintenance, and Error.


⚙️ Functionalities
Real-time machine monitoring via CLI.
Inventory and resource management.
Emergency handling and safety protocols.
Smart production scheduling.

🖥️ Interface
CLI Dashboard: For plant control and monitoring.
