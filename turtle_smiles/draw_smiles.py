#!/usr/bin/env python3


#MIT License
#
#Copyright (c) 2018 Matthijs Jonathan Tadema
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

desc = """
This script takes a molecule in the form of a smiles string and tries to draw
it using turtle graphics. It is currently limited to molecules with a single hexagonal ring and at most carbon atoms with a valence of 3
"""

# Try to import read_smiles
try:
    # Otherwise demand that the user installs it
    from pysmiles import read_smiles
except ImportError as e:
    print("Please get pysmiles from https://github.com/pckroon/pysmiles")
import turtle_smiles.structure as structure
import turtle_smiles.draw as draw

def main():
    # Parse command line arguments to get a smiles string
    args = parse_arguments()
    if not args.smiles_string:
        smiles_string = dict_aa[args.mol]
    else:
        smiles_string = args.smiles_string

    print("Drawing molecule:\n{}".format(smiles_string))

    # Parse the string into a graph object
    g = read_smiles(smiles_string)
    # Mark the cyclic edges as rings
    try:
        g = structure.mark_rings(g)
    except:
        pass

    # init turtle window and start drawing, wait for window events
    draw.init()
    draw.molecule(g)
    draw.done()

def parse_arguments():
    from argparse import ArgumentParser
    parser = ArgumentParser(
            description = desc)
    parser.add_argument("-mol", dest="mol", metavar="mol_from_dict", default = "A",
            help="Pick a molecule from the dictionary", choices = dict_aa.keys(), type=str)
    parser.add_argument("-s", dest="smiles_string", type=str,
            help="A molecule in smiles notation, will override the \"mol\" argument")
    return parser.parse_args()

# A dictionary that holds several molecules that are tested to work
dict_aa = {
        #"Y": "N[C@@H](Cc1ccc(O)cc1)C(O)=O",
        "F": "C1=CC=C(C=C1)CC(C(=O)O)N",
        "R": "NC(CCCNC(N)=N)C(O)=O",
        "C": "C([C@@H](C(=O)O)N)S",
        "G": "C(C(=O)O)N",
        "K": "C(CCN)CC(C(=O)O)N",
        "D": "O=C(O)CC(N)C(=O)O",
        "E": "C(C(C(=O)O)N)C(=O)O",
        "S": "C([C@@H](C(=O)O)N)O",
        "T": "C[C@H]([C@@H](C(=O)O)N)O",
        "N": "C([C@@H](C(=O)O)N)C(=O)N",
        "Q": "O=C(N)CCC(N)C(=O)O",
        "A": "O=C(O)C(N)C",
        "V": "CC(C)[C@@H](C(=O)O)N",
        "I": "CC[C@H](C)[C@@H](C(=O)O)N",
        "L": "CC(C)C[C@@H](C(=O)O)N",
        "M": "CSCC[C@H](N)C(=O)O",
        "gluc": "C([C@@H]1[C@H]([C@@H]([C@H]([C@H](O1)O)O)O)O)O",
        "stearin": """CCCCCCCCCCCCCCCCCC(=O)OCC(COC(=O)CCCCCCCCCCCCCCCCC)OC(=O)CCCCCCCCCCCCCCCCC"""
        }

if __name__ == "__main__":
    main()
