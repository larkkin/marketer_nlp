# marketer_nlp


This repository contains project files (`InformationExtractor.py, Property.py, PropertyComparator.py`), config files, unit test files (`test_information_extractor.py, test_property_comparator.py`), a file with input texts (`test_texts.txt`) and `run.py` which, being executed (`python run.py`), prints solutions to Task 1 and Task 2.

The only dependency is the Spacy library that is available via pip (`python -m pip install spacy`).
I chose Spacy over other packages (like NLTK or Stanza) because the task was focused on good code quality, good architecture and maintainability. Under these conditions, Spacy is the best option: it is designed to be used in industrial applications (unlike research-oriented NLTK and Stanza), is well supported, documented, and allows for building modular pipelines. 
