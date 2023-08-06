class PhyloTree:
    def __init__(self, tree_Newick: str = None) -> None:
        self.tree = str(tree_Newick)
        return

    def save(self, file_name: str) -> None:
        """
        Save the tree to a file in Newick format
        """

        with open(file_name, "w") as text_file:
            text_file.write(self.tree)
        return
