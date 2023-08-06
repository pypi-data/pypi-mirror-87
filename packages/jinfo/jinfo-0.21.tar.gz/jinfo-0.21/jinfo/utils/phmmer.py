from typing import Union, List
from jinfo.alignment import BaseAlignment
from jinfo.sequence import BaseSeq, DNASeq, RNASeq, AASeq

ALL_SEQS = Union[BaseSeq, DNASeq, RNASeq, AASeq]


class HmmerNotInstalledError(Exception):
    pass


def seq_id_from_hmmer(result_path: str, seq_obj: ALL_SEQS = BaseSeq) -> ALL_SEQS:
    """"""

    return seq_obj()


def phmmer(seq_list: List[ALL_SEQS], query_seq: ALL_SEQS) -> ALL_SEQS:
    """

    ***Requires hmmer package***
    Returns:
    """

    import subprocess
    import multiprocessing as mp
    from jinfo.utils.seq_list_to_fasta import seq_list_to_fasta
    from jinfo.utils.seq_list_from_fasta import seq_list_from_fasta

    try:
        test_cmd = "phmmer".split(" ")
        subprocess.run(test_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        raise HmmerNotInstalledError

    q_path = "_hmmer_temp_query.fasta"
    db_path = "_hmmer_temp_db.fasta"
    out_path = "_hmmer_temp_out.txt"

    query_seq.save_fasta(q_path)
    seq_list_to_fasta(seq_list=seq_list, file_name=db_path, label_list=None)

    bash_cmd = f"phmmer {q_path} {db_path} -o {out_path} -cpu {mp.cpu_count()}".split(
        sep=" "
    )
    subprocess.run(bash_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Get result from hmmer output fule...
    hit_id = seq_id_from_hmmer(out_path)
    output_seq_obj = 0

    cleanup_cmd = f"rm {q_path} {db_path} {out_path}".split(sep=" ")
    subprocess.run(cleanup_cmd)
    return


if __name__ == "__main__":
    pass
