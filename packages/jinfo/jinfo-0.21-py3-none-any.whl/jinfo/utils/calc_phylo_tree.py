from jinfo.alignment import BaseAlignment
from jinfo.phylogenetics import PhyloTree


class FastTree2NotInstalledError(Exception):
    pass


def calc_phylo_tree(alignment_obj: BaseAlignment) -> PhyloTree:
    """
    Calculate a Newick format phylogenetic tree from an alignment object

    ***Requires FastTree2 package***
    Returns: Tree object
    """

    import subprocess
    from jinfo.utils.seq_list_to_fasta import seq_list_to_fasta

    try:
        test_cmd = "fasttreeMP".split(" ")
        subprocess.run(test_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        raise FastTree2NotInstalledError

    in_path = "temp.fasta"
    out_path = "temp.tree"
    seq_list_to_fasta(
        seq_list=alignment_obj.seqs, file_name=in_path, label_list=alignment_obj.labels
    )

    bash_cmd = f"fasttreeMP {in_path}".split(sep=" ")
    with open(out_path, "w") as text_file:
        subprocess.run(bash_cmd, stdout=text_file)

    with open(out_path, "r") as text_file:
        tree_obj = PhyloTree(text_file.read())

    cleanup_cmd = f"rm {in_path} {out_path}".split(sep=" ")
    subprocess.run(cleanup_cmd)
    return tree_obj


if __name__ == "__main__":
    pass
