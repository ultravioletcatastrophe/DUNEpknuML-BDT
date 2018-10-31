# DUNEpknuML-BDT
Scripts which use machine learning techniques to evaluate ROOT files in order to differentiate proton decay and charged current neutrino background interactions.

Use ttree_create_split.py to generate the training and testing trees, classification.py or classification_BDT.py can read those and produce a set of weights which can be evaluated by reader.py or reader_BDT.py respectively.
