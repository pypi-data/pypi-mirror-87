from jinfo.alignment import BaseAlignment


def remove_degenerate_seqs(
    alignment_obj: BaseAlignment, identity_limit: int, show_id_array: bool = False
) -> BaseAlignment:
    """
    Filter high similarity sequences from a list of Seq objects

    Returns: BaseAlignment
    """
    import multiprocessing as mp
    from functools import partial
    from jinfo.utils.percentage_identity import percentage_identity

    seq_list = alignment_obj.seqs
    identity_array = []
    filtered_seqs = []
    pool = mp.Pool(mp.cpu_count())  # Set up cpu pool for parallel calculation

    for seq_obj in seq_list:
        id_partial = partial(percentage_identity, seq2=seq_obj)
        identity_array_row = pool.map(id_partial, seq_list)
        identity_array.append(identity_array_row)

    if show_id_array:
        print("Calculated alignment identity array:")
        for i, row in enumerate(identity_array):
            print(f"{seq_list[i].label}\t{row}")

    for i, row in enumerate(identity_array):
        row.remove(100)  # remove seq 100% match with itself
        if max(row) < float(identity_limit):
            filtered_seqs.append(seq_list[i])

    return BaseAlignment(filtered_seqs)


if __name__ == "__main__":
    pass
