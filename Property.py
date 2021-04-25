class Property:
    def __init__(self, modifiers, floor, have_balcony):
        self.modifiers = modifiers
        self.floor = floor
        self.have_balcony = have_balcony
    
    def print_modifiers(self):
        for key, value in self.modifiers.items():
            print(f"\t{key}: {', '.join(value)}")