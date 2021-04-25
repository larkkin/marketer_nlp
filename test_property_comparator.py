import json
from unittest import TestCase
from InformationExtractor import InformationExtractor
from PropertyComparator import PropertyComparator

class TestPropertyComparator(TestCase):
    default_config_filename = "default_config.json"
    
    def load_config(self):
        with open(self.default_config_filename) as inp:
            config = json.load(inp)
        return config
    
    def test_load_invalid_config(self):
        with self.assertRaises(KeyError):
            property_comparator = PropertyComparator.load_from_config({})

    def test_load_valid_config(self):
        config = self.load_config()
        property_comparator = PropertyComparator.load_from_config(config)
        self.assertDictEqual(property_comparator.modifier_weights,
                             {"bathroom": 1.0,
                              "bedroom": 1.0,
                              "living room": 1.0,
                              "property": 1.0,
                              "garden": 1.0,
                              "location": 1.0})
        self.assertEqual(property_comparator.floor_weight, 1.0)
        self.assertEqual(property_comparator.balcony_weight, 1.0)

    def test_compare_same(self):
        config = self.load_config()
        information_extractor = InformationExtractor.load_from_config(config)
        property_comparator = PropertyComparator.load_from_config(config)
        text = "A spacious apartment with one bedroom and a nice balcony"
        property_instance = information_extractor.make_property(text)
        similarity = property_comparator.similarity(property_instance, property_instance, normalize=True)
        self.assertEqual(similarity, 1.0)
    
    def test_compare_different(self):
        config = self.load_config()
        information_extractor = InformationExtractor.load_from_config(config)
        property_comparator = PropertyComparator.load_from_config(config)
        text_1 = "A spacious apartment with one bedroom, two bathrooms, light reception and a nice balcony"
        property_instance_1 = information_extractor.make_property(text_1)
        text_2 = "A ground floor apartment with one bathrooms, a lovely tiny garden and atrractive location"
        property_instance_2 = information_extractor.make_property(text_2)
        similarity = property_comparator.similarity(property_instance_1, property_instance_2, normalize=True)
        self.assertEqual(similarity, 0.0)