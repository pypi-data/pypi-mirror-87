from jinfo import DNASeq


def random_DNASeq(seq_length: int) -> DNASeq:
    """
    Generate a random DNA sequence

    Returns: random DNASeq of length seq_length
    """

    import random
    from jinfo.sequence import DNASeq

    dna_base_list = ["A", "T", "C", "G"]
    seq_list = [random.choice(dna_base_list) for i in range(seq_length)]
    return DNASeq(sequence="".join(seq_list))


if __name__ == "__main__":
    pass
