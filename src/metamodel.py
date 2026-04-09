from textx import metamodel_from_file

import os

def create_metamodel():
    grammar = os.path.join(os.path.dirname(__file__), 'arch.tx')
    return metamodel_from_file(grammar)
