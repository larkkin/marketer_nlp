import json
from Property import Property
from InformationExtractor import InformationExtractor
from PropertyComparator import PropertyComparator



def main():
    with open("config.json") as inp:
        config = json.load(inp)
    information_extractor = InformationExtractor.load_from_config(config)
    property_comparator = PropertyComparator.load_from_config(config)
    with open("test_text.json") as inp:
        input_texts = json.load(inp)
    properties = [information_extractor.make_property(text) for text in input_texts]

    print("\n== Task 1 ==")
    for i, p in enumerate(properties):
        print(f"Property {i+1}")
        p.print_modifiers()

    similarity_matrix = [[property_comparator.similarity(p1, p2) for p1 in properties] for p2 in properties]
    print("\n== Task 2 ==")
    print('\n'.join([' '.join([str(x).ljust(6) for x in row]) for row in similarity_matrix]))

if __name__ == "__main__":
    main()