from typing import Union, List, Optional
from jinfo.sequence import BaseSeq, DNASeq, RNASeq, AASeq

ANY_SEQ = Union[BaseSeq, DNASeq, RNASeq, AASeq]


def seq_list_to_fasta(
    seq_list: List[ANY_SEQ], file_name: Optional[str], label_list: Optional[List[str]]
) -> str:
    """
    Convert a list of Seq objects to a fasta format string

    Optionally add labels and save to file
    Returns: fasta string
    """

    fasta_str = ""
    for i, seq_obj in enumerate(seq_list):
        if label_list:
            label = label_list[i]
        elif seq_obj.label != "":
            label = seq_obj.label
        else:
            label = f"Sequence_{i}"
        fasta_str += f">{label}\n{seq_obj.seq}\n\n"

    if file_name:
        with open(file=file_name, mode="w") as text_file:
            text_file.write(fasta_str)
    return fasta_str


if __name__ == "__main__":
    pass
