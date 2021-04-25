import spacy

from Property import Property

class InformationExtractor:
    def __init__(self,
                 categories,
                 text_to_number,
                 balcony_synonyms,
                 modifiers_of_interest=("nummod", "amod"),
                 model="en_core_web_sm"):
        self.categories = categories
        self.noun_to_category = {noun: category for category, noun_list in categories.items() \
                                     for noun in noun_list}
        self.text_to_number = text_to_number
        self.balcony_synonyms = balcony_synonyms
        self.modifiers_of_interest = modifiers_of_interest
        self.model = spacy.load(model)
    
    @staticmethod
    def load_from_config(config):
        return InformationExtractor(config["categories"],
                                    config["text_to_number"],
                                    config["balcony_synonyms"])

    def parse_text(self, text):
        return self.model(text)

    def parse_number(self, text_number):
        if text_number in self.text_to_number:
            return self.text_to_number[text_number]
        return text_number
    
    def extract_modifiers(self, parsed_text, mods):
        modifiers_by_noun = {key: set() for key in self.noun_to_category}
        modifiers_by_category = {key: set() for key in self.categories}
        for token in parsed_text:
            if token.head.pos_ == "NOUN" and token.head.lemma_ in self.noun_to_category.keys():
                lemma = token.lemma_
                if token.dep_ == "nummod":
                    lemma = self.parse_number(lemma)
                if token.dep_ in mods:
                    modifiers_by_noun[token.head.lemma_].add(lemma)
        for noun, modifier_set in modifiers_by_noun.items():
            category = self.noun_to_category[noun]
            modifiers_by_category[category].update(modifier_set)
        return modifiers_by_category
    
    def extract_floor(self, parsed_text):
        modifiers = set()
        for token in parsed_text:
            if token.head.pos_ == "NOUN" and token.head.lemma_ == "floor":
                if token.dep_ == "nummod" or (token.dep_ == "compound" and token.lemma_ in self.text_to_number):
                    modifiers.add(self.parse_number(token.lemma_))
        if modifiers:
            return max(modifiers)
        return "?"
    
    def has_balcony(self, parsed_text):
        for token in parsed_text:
            if token.lemma_ in self.balcony_synonyms:
                return True
        return False
    
    def make_property(self, text):
        parsed_text = self.parse_text(text)
        modifiers = self.extract_modifiers(parsed_text, mods=self.modifiers_of_interest)
        floor = self.extract_floor(parsed_text)
        has_balcony = self.has_balcony(parsed_text)
        properties = Property(modifiers, floor, has_balcony)
        return properties