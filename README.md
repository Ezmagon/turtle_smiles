# Turtle_smiles
Smiles is a method of encoding chemical structures into a single string.
turtle_smiles takes a molecule in the form of a smiles string and tries to draw it using turtle graphics. 
It is currently limited to molecules with a single hexagonal ring and at most carbon atoms with a valence of 3

Requirements:
This package requires the pysmiles package to parse smiles strings. It can be found [here](https://github.com/pckroon/pysmiles)

Installation:
Clone the repo and run `python3 setup.py install`

Usage:
After installation, run `draw_smiles.py -h` for instructions

Example:
An example of what turtle\_smiles can do
![alt text](https://github.com/Ezmagon/turtle_smiles/blob/master/example.png "Phenylalanine as drawn by turtle\_smiles")
