from jinfo.sequence import DNASeq


def DNASeq_from_NCBI(NCBI_accession: str) -> DNASeq:
    """
    Fetch a DNA sequence using the NCBI Entrez api

    Returns jinfo.DNASeq object
    """

    return DNASeq()


if __name__ == "__main__":
    pass
