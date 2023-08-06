from typing import Union, List
from jinfo.alignment import BaseAlignment
from jinfo.sequence import BaseSeq, DNASeq, RNASeq, AASeq

ALL_SEQS = Union[BaseSeq, DNASeq, RNASeq, AASeq]


class MuscleNotInstalledError(Exception):
    pass


def multialign(seq_list: List[ALL_SEQS], maxiters: int = 16) -> BaseAlignment:
    """
    Perform multiple sequence alignment, optionally control the number of iterations

    ***Requires MUSCLE package***
    Returns Alignment object
    """

    import subprocess
    from jinfo.utils.seq_list_to_fasta import seq_list_to_fasta
    from jinfo.utils.alignment_from_fasta import alignment_from_fasta

    try:
        test_cmd = "muscle -quiet".split(" ")
        subprocess.run(test_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        raise MuscleNotInstalledError

    in_path = "_temp.fasta"
    out_path = "_temp2.fasta"
    seq_list_to_fasta(seq_list=seq_list, file_name=in_path, label_list=None)
    bash_cmd = f"muscle -in {in_path} -out {out_path} -quiet -maxiters {maxiters}".split(
        sep=" "
    )
    subprocess.run(bash_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    alignment_obj = alignment_from_fasta(out_path, seq_obj=type(seq_list[0]))
    cleanup_cmd = f"rm {in_path} {out_path}".split(sep=" ")
    subprocess.run(cleanup_cmd)
    return alignment_obj


if __name__ == "__main__":
    pass
