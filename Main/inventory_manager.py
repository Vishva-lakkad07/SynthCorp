
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

class InventoryObserver:
    def update(self, resource_name, quantity):
        pass


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
            cls.resources = {}
            cls.observers = []
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

# Example usage
if __name__ == "__main__":
    inventory = InventoryManager()
    ordering = OrderingSystem()
    inventory.add_observer(ordering)
    inventory.add_resource("Steel", 20, 10)
    inventory.update_stock("Steel", -15)  # Drops to 5, triggers reorder

    legacy = LegacyInventory()
    adapter = LegacyInventoryAdapter(legacy)
    print(f"Legacy stock for Steel: {adapter.get_quantity('Steel')}")