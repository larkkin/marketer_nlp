import json
from unittest import TestCase
from InformationExtractor import InformationExtractor

class TestInformationExtractor(TestCase):
    default_config_filename = "default_config.json"
    
    def load_config(self):
        with open(self.default_config_filename) as inp:
            config = json.load(inp)
        return config
    
    def test_load_invalid_config(self):
        with self.assertRaises(KeyError):
            information_extractor = InformationExtractor.load_from_config({})

    def test_load_valid_config(self):
        config = self.load_config()
        information_extractor = InformationExtractor.load_from_config(config)
        self.assertDictEqual(information_extractor.categories, config["categories"])
        self.assertDictEqual(information_extractor.text_to_number, config["text_to_number"])
        parsed_sentence = information_extractor.model("I am a spacy model")
        self.assertEqual(len(parsed_sentence), 5)

    def test_make_property(self):
        config = self.load_config()
        information_extractor = InformationExtractor.load_from_config(config)
        text = "A spacious apartment with one bedroom and a nice balcony"
        property_instance = information_extractor.make_property(text)
        self.assertDictEqual(property_instance.modifiers,
                             {"bathroom": set(),
                              "bedroom": {"1"},
                              "living room": set(),
                              "property": {"spacious"},
                              "garden": set(),
                              "location": set()})
        self.assertEqual(property_instance.floor, "?")
        self.assertTrue(property_instance.have_balcony)
