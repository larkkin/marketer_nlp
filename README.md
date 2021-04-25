# marketer_nlp


This repository contains project files (`InformationExtractor.py, Property.py, PropertyComparator.py`), config files, unit test files (`test_information_extractor.py, test_property_comparator.py`), a file with input texts (`test_texts.txt`) and `run.py` which, being executed (`python run.py`), prints solutions to Task 1 and Task 2.

The only dependency is the Spacy library that is available via pip (`python -m pip install spacy`).
I chose Spacy over other packages (like NLTK or Stanza) because the task was focused on good code quality, good architecture and maintainability. Under these conditions, Spacy is the best option: it is designed to be used in industrial applications (unlike research-oriented NLTK and Stanza), is well supported, documented, and allows for building modular pipelines. 

The similarity function is based on three components: 
1) modifiers (adjectives/numbers) corresponding to the nouns of interest. Since modifier detection is fuzzy, I consider a non-empty intersection of the modifier sets for a given category as a positive evidence for similarity. In other words, if in one description, the bathroon is _spacious_ and _refurbished_, and in another one, there are _two_ _spacious_ _light_ bathrooms, I increase the overall similarity by 1. If in both descriptions, there are two spacious light bathrooms, I still increase the overall similarity by 1.
2) floor: I extract the information about the floors the properties are located on from the descriptions and then increase increase the overall similarity by 1 if the floors are the same.
3) balcony: I detect if there are balconies/terraces in the properties from the descriptions and then increase increase the overall similarity by 1 if both/neither of the properties have a balcony/terrace.
The result similarity is then by default normalized by the maximum possible one, so that the total score is always between 0 and 1.
The weight of each modifier, floor, or balcony is loaded from a config file. In other words, if both/neither of the properties have a balcony, the similarity is increased not by 1 but by the balcony_weight value defined in the config file. This way, the user can define what is more for them.
Other components can be easily added to the project. 