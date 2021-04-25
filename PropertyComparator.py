class PropertyComparator:
    def __init__(self, modifier_weights, floor_weight, balcony_weight):
        self.modifier_weights = modifier_weights
        self.floor_weight = floor_weight
        self.balcony_weight = balcony_weight
        
    @staticmethod
    def load_from_config(config):
        return PropertyComparator(config["modifier_weights"],
                                  config["floor_weight"],
                                  config["balcony_weight"])
    
    def similarity(self, property_1, property_2, normalize=True):
        similarity = 0
        for key, weight in self.modifier_weights.items():
            have_intersection = len(property_1.modifiers[key] & property_2.modifiers[key]) > 0 or len(property_1.modifiers[key] | property_2.modifiers[key]) == 0
            similarity += have_intersection * weight
        similarity += (property_1.floor == property_2.floor) * self.floor_weight
        similarity += (property_1.have_balcony == property_2.have_balcony) * self.balcony_weight
        if normalize:
            max_possible_similarity = sum(self.modifier_weights.values()) + self.floor_weight + self.balcony_weight
            similarity /= max_possible_similarity
        return similarity