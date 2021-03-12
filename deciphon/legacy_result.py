__all__ = ["legacy_result"]


def legacy_result(r):
    path = r.alt_stream
    pos = 0
    frag_start = 0
    frag_end = 0
    matching = False
    dna_intervals = []
    for step in path.split(","):
        state = step.split(":")[0]
        size = int(step.split(":")[1])
        if state == "E" and matching:
            matching = False
            frag_end = pos
            dna_intervals.append((frag_start, frag_end))
        if state == "B":
            matching = True
            frag_start = pos
        pos += size

    path = r.alt_stream
    pos = 0
    frag_start = 0
    frag_end = 0
    matching = False
    cfragments = []
    cstream = r.alt_codon_stream
    for step in path.split(","):
        state = step.split(":")[0]
        size = int(step.split(":")[1])
        if size > 0:
            size = 3
        if state == "E" and matching:
            matching = False
            frag_end = pos
            cfragments.append(cstream[frag_start:frag_end])
        if state == "B":
            matching = True
            frag_start = pos
        pos += size

    path = r.alt_stream
    pos = 0
    frag_start = 0
    frag_end = 0
    matching = False
    afragments = []
    astream = r.alt_amino_stream
    for step in path.split(","):
        state = step.split(":")[0]
        size = int(step.split(":")[1])
        if size > 0:
            size = 1
        if state == "E" and matching:
            matching = False
            frag_end = pos
            afragments.append(astream[frag_start:frag_end])
        if state == "B":
            matching = True
            frag_start = pos
        pos += size

    return dna_intervals, cfragments, afragments
