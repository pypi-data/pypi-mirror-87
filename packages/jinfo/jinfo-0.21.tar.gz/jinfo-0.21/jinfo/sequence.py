from jinfo.tables import (
    DNA_VOCAB,
    RNA_VOCAB,
    AA_VOCAB,
    CODON_TABLE,
    RC_TABLE,
    NT_MW_TABLE,
    AA_MW_TABLE,
)


class SeqVocabError(Exception):
    pass


class SeqLengthError(Exception):
    pass


class UnknownBaseError(Exception):
    pass


class BaseSeq:
    """
    Parent class for DNA/RNA/AA sequence objects
    """

    def __init__(self, sequence: str = "", label: str = "", vocab: set = None) -> None:
        self.vocab = vocab
        self.label = label
        self.update_seq(sequence)
        self.len = len(self.seq)
        return

    def __str__(self):
        return f"{self.label}\t{self.seq}"

    def check_seq_valid(self) -> None:
        """
        Ensure that the sequence string is consistant with the vocab
        """

        if self.vocab is not None:
            if not self.vocab.issuperset(set(self.new_seq)):
                raise SeqVocabError("Seq contains bases not in vocab")
        return

    def update_seq(self, sequence: str = "") -> None:
        """
        Replace the sequence string with a new string
        """

        self.new_seq = sequence.upper()
        self.check_seq_valid()
        self.seq = self.new_seq
        self.len = len(sequence)
        return

    def update_label(self, label: str = "") -> None:
        """
        Replace the sequence string with a new string
        """

        self.label = label
        return

    def align(self, seq2, maxiters: int = 16):
        """
        Perform alignment of two sequences, optionally control the number of iterations

        ***Requires MUSCLE package***
        Returns Alignment object
        """

        from jinfo.utils.multialign import multialign

        return multialign([self, seq2], maxiters=maxiters)

    def identity(self, seq2) -> float:
        """
        Calculate the percentage identity between two sequences

        Returns: float
        """
        from jinfo.utils.percentage_identity import percentage_identity

        return percentage_identity(self, seq2)

    def save_fasta(self, file_name: str) -> None:
        """
        Save sequence to fasta file
        """

        import textwrap

        seq_formatted = textwrap.fill(self.seq, width=80)
        if self.label == "":
            out_label = "jinfo_sequence"
        else:
            out_label = self.label

        with open(file_name, "w") as text_file:
            text_file.write(f">{out_label}\n{seq_formatted}")
        return


class DNASeq(BaseSeq):
    """
    Class to hold sequences of DNA
    """

    def __init__(self, sequence: str = "", label: str = "") -> None:
        """
        Call the superclass constructor with new default vocab argument
        """

        super(DNASeq, self).__init__(sequence=sequence, label=label, vocab=DNA_VOCAB)
        return

    def transcribe(self) -> str:
        """
        Returns: RNA transcript of the DNA sequence
        """

        return self.seq.replace("T", "U")

    def translate(self) -> str:
        """
        Returns: translated protein sequence of the DNA sequence
        """

        transcript = self.transcribe()
        if len(transcript) % 3 != 0:
            raise SeqLengthError("Seq cannot be split into codons, not a multiple of 3")
        codon_list = [transcript[i : i + 3] for i in range(0, len(transcript), 3)]
        return "".join([CODON_TABLE[codon] for codon in codon_list])

    def reverse_complement(self) -> str:
        """
        Returns: reverse complement of the DNA sequence
        """

        return "".join([RC_TABLE[base] for base in self.seq][::-1])

    def find_CDS(self):
        return

    def MW(self) -> float:
        """
        Calculate MW of linear double stranded DNA

        Returns: Molecular weight float
        """

        if "X" in self.seq:
            raise UnknownBaseError("X base in sequence")
        fw_mw = sum([NT_MW_TABLE[base] for base in self.seq]) + 17.01
        rv_mw = sum([NT_MW_TABLE[base] for base in self.reverse_complement()]) + 17.01
        return fw_mw + rv_mw

    def GC(self, dp: int = 2) -> float:
        """
        Calculate the GC% of the DNA sequence with optional arg to control precision

        Returns: GC percentage float
        """

        return round(100 * (self.seq.count("C") + self.seq.count("G")) / self.len, dp)

    def tm(self, dp: int = 2) -> float:
        """
        Calculate DNA sequence tm with optional arg to control precision

        Returns: melting temperature float
        """

        import primer3

        return round(primer3.calcTm(self.seq), dp)

    def one_hot(self, max_len: int = None):
        """
        
        """
        from jinfo import one_hot_dna

        if max_len:
            return one_hot_dna(self, max_len)
        else:
            return one_hot_dna(self, self.len)


class RNASeq(BaseSeq):
    """
    Class to hold RNA sequences
    """

    def __init__(self, sequence: str = "", label: str = "") -> None:
        """
        Call the superclass constructor with new default vocab argument
        """

        super(RNASeq, self).__init__(sequence=sequence, label=label, vocab=RNA_VOCAB)
        return

    def reverse_transcribe(self) -> str:
        """
        Returns: DNA template of the RNA sequence
        """

        return self.seq.replace("U", "T")

    def translate(self) -> str:
        """
        Returns: the translated protein sequence of the DNA sequence
        """

        if len(self.seq) % 3 != 0:
            raise SeqLengthError("Seq cannot be split into codons, not a multiple of 3")
        codon_list = [self.seq[i : i + 3] for i in range(0, len(self.seq), 3)]
        return "".join([CODON_TABLE[codon] for codon in codon_list])

    def MW(self) -> float:
        """
        Calculate MW of single stranded RNA

        Returns: Molecular weight float
        """

        if "X" in self.seq:
            raise UnknownBaseError("X base in sequence")
        return sum([NT_MW_TABLE[base] for base in self.seq]) + 17.01


class AASeq(BaseSeq):
    """
    Class to hold amino acid sequences
    """

    def __init__(self, sequence: str = "", label: str = ""):
        """
        Call the superclass constructor with new default vocab argument
        """

        super(AASeq, self).__init__(sequence=sequence, label=label, vocab=AA_VOCAB)
        return

    def MW(self) -> float:
        """
        Calculate protein MW

        Returns: Molecular weight float
        """

        if "X" in self.seq:
            raise UnknownBaseError("X residue in sequence")
        return sum([AA_MW_TABLE[base] for base in self.seq])


if __name__ == "__main__":
    pass
