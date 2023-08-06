from typing import Union
from jinfo.sequence import BaseSeq, DNASeq, RNASeq, AASeq

ALL_SEQS = Union[BaseSeq, DNASeq, RNASeq, AASeq]


def percentage_identity(seq1: ALL_SEQS, seq2: ALL_SEQS, dp: int = 2) -> float:
    """
    Calculate pairwise sequence similarity from aligned sequences

    Optionally control precision using dp argument
    Returns: float
    """
    i = 0
    for b1, b2 in zip(seq1.seq, seq2.seq):
        if b1 == b2:
            i += 1
    pid = i * 100 / ((seq1.len + seq2.len) / 2)
    return round(pid, dp)


if __name__ == "__main__":
    pass
