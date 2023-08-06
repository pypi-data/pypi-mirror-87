from typing import Union, Optional
from jinfo.sequence import BaseSeq, DNASeq, RNASeq, AASeq

ANY_SEQ = Union[BaseSeq, DNASeq, RNASeq, AASeq]


def seq_from_fasta(file_path: str, seq_type: Optional[ANY_SEQ]) -> ANY_SEQ:
    """
    Parse a fasta file

    Returns specified type of Seq object
    """

    import re
    from jinfo.sequence import BaseSeq, DNASeq, RNASeq, AASeq

    with open(file_path, "r") as text_file:
        fasta_str = text_file.read()

    label = re.findall(r"^>(.*)", fasta_str)[0]
    fasta_lines = fasta_str.split("\n")
    label_index = fasta_lines.index(">" + label)
    seq_string = "".join(fasta_lines[label_index + 1 :])
    if seq_type is None:
        return BaseSeq(sequence=seq_string, label=label)
    else:
        return seq_type(sequence=seq_string, label=label)


if __name__ == "__main__":
    pass
