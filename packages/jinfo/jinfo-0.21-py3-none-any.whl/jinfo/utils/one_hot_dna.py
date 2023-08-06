from jinfo.sequence import DNASeq
from numpy import array


class SeqLengthError(Exception):
    pass


def one_hot_dna(seq_obj: DNASeq, max_seq_len: int) -> array:
    """
    One hot encode a DNASeq sequence for ML applications.

    Add zero padding up to the maximum length.
    Returns: 1D numpy array of length 4*max_seq_len
    """

    import numpy as np

    if seq_obj.len > max_seq_len:
        raise SeqLengthError("DNASeq.len exceeds max_seq_len")

    encode_dict = {
        "A": [1, 0, 0, 0],
        "T": [0, 1, 0, 0],
        "C": [0, 0, 1, 0],
        "G": [0, 0, 0, 1],
        "X": [0, 0, 0, 0],
    }
    padding = "".join(["X" for i in range(max_seq_len - seq_obj.len)])
    encoded_dna = [encode_dict[base] for base in seq_obj.seq + padding]
    np_encoded = np.array(encoded_dna, dtype=int)
    return np_encoded.flatten()


if __name__ == "__main__":
    pass
