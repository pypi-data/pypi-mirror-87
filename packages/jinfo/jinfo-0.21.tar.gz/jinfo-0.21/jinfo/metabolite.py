class BaseMetabolite:
    def __init__(self, smiles: str = None, name: str = None) -> None:
        self.smiles = smiles
        self.name = name
        return
