from typing import Union, Optional

from jinfo.alignment import BaseAlignment
from jinfo.sequence import BaseSeq, DNASeq, RNASeq, AASeq

ANY_SEQ = Union[BaseSeq, DNASeq, RNASeq, AASeq]


def alignment_from_fasta(file_path: str, seq_obj: ANY_SEQ = BaseSeq) -> BaseAlignment:
    """
    Parse alignment from fasta file

    Returns Alignment object
    """

    from jinfo.utils.seq_list_from_fasta import seq_list_from_fasta

    seq_list = seq_list_from_fasta(file_path=file_path, seq_obj=seq_obj)
    return BaseAlignment(aligned_sequences=seq_list)


if __name__ == "__main__":
    pass
