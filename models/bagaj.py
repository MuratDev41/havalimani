class Baggage:
    
    def __init__(self):
        
        self.items = []
        
    def add_item(self, item_name, is_dangerous=False):
        
        self.items.append({
            "item": item_name,
            "dangerous": is_dangerous
        })
    
    def get_items(self):
        
        return self.items
    
    def has_dangerous_items(self):
        
        for item in self.items:
            if item["dangerous"]:
                return True
        return False
    
    def get_dangerous_items(self):
        
        return [item for item in self.items if item["dangerous"]]
    
    def count_items(self):
        
        return len(self.items)

def inspect_baggage(baggage, inspection_func=None):
   
    if inspection_func:
        
        return inspection_func(baggage)
    
    
    dangerous_items = baggage.get_dangerous_items()
    is_safe = len(dangerous_items) == 0
    
    return is_safe, dangerous_items