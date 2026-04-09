from src.transformations import apply_transformations
from src.metamodel import create_metamodel

import os

if __name__ == '__main__':
    metamodel = create_metamodel()

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    model_path = os.path.join(BASE_DIR, 'model.arch')
    model = metamodel.model_from_file(model_path)
    apply_transformations(model)
