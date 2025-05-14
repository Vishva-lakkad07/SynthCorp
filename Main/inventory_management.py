class Resource:
    def __init__(self, name, quantity, reorder_threshold):
        self._name = name
        self._quantity = quantity
        self._reorder_threshold = reorder_threshold

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        self._quantity = value

    @property
    def reorder_threshold(self):
        return self._reorder_threshold

# Observer interface
class InventoryObserver:
    def update(self, resource_name, quantity):
        pass

# Concrete observer for ordering system
class OrderingSystem(InventoryObserver):
    def update(self, resource_name, quantity):
        if quantity < 10:  # Example threshold
            print(f"Ordering more {resource_name}...")

# Singleton Inventory Manager
class InventoryManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(InventoryManager, cls).__new__(cls)
            cls._instance.resources = {"steel": Resource("steel", 1000, 100), "plastic": Resource("plastic", 500, 100)}
            cls._instance.observers = [OrderingSystem()]
        return cls._instance

    def add_resource(self, name, quantity, reorder_threshold):
        self.resources[name] = Resource(name, quantity, reorder_threshold)

    def add_observer(self, observer):
        self.observers.append(observer)

    def update_stock(self, resource_name, amount):
        if resource_name in self.resources:
            resource = self.resources[resource_name]
            resource.quantity += amount
            for observer in self.observers:
                observer.update(resource_name, resource.quantity)

    def check_inventory(self):
        print("Checking inventory levels...")
        for resource_name, resource in self.resources.items():
            if resource.quantity < resource.reorder_threshold:
                print(f"Low inventory warning: {resource_name} at {resource.quantity} units")

    def show_inventory(self):
        print("Current Inventory:")
        for resource_name, resource in self.resources.items():
            print(f"{resource_name}: {resource.quantity} units")

    def consume_material(self, material, quantity):
        if material in self.resources and self.resources[material].quantity >= quantity:
            self.resources[material].quantity -= quantity
            print(f"Consumed {quantity} units of {material}")
            for observer in self.observers:
                observer.update(material, self.resources[material].quantity)
        else:
            print(f"Insufficient {material} in inventory")

# Legacy inventory system (example)
class LegacyInventory:
    def get_stock(self, item):
        return 50  # Dummy data

# Adapter for legacy system
class LegacyInventoryAdapter:
    def __init__(self, legacy_inventory):
        self.legacy_inventory = legacy_inventory

    def get_quantity(self, resource_name):
        return self.legacy_inventory.get_stock(resource_name)