from pathlib import Path

import fasta_reader as fr

import deciphon as dcp


def scan_rob(db_filepath, fasta_filepath):
    # db = "/Users/horta/tmp/oi/Pfam-A_4.dcp"
    # dna_fasta = "/Users/horta/tmp/oi/dna.fasta"
    # amino.fasta  codon.fasta  data.json  data.py  dna.fasta  output.gff  Pfam-A_4.dcp

    multiple_hits = True
    hmmer3_compat = False
    task = dcp.Task(True, True, multiple_hits, hmmer3_compat)
    tgt_id = []
    targets = []
    for tgt in fr.read_fasta(fasta_filepath):
        task.add(tgt.sequence.encode())
        targets.append(tgt.sequence.encode())
        tgt_id.append(tgt.id)

    server = dcp.Server(Path(db_filepath))
    server.scan(task)
    task_result = task.result
    ritems = []
    for r in task_result.results:
        target_id = tgt_id[r.seqid]
        profile_acc = server.metadata(r.profid).acc
        profile_name = server.metadata(r.profid).name
        dna_intervals, cfragments, afragments = dcp.legacy_result(r)
        for i, cfrag, afrag in zip(dna_intervals, cfragments, afragments):
            ritems.append(
                (target_id, i[0], i[1], profile_name, profile_acc, cfrag, afrag)
            )

    ritems = sorted(ritems, key=lambda i: (i[0], i[1], i[2], i[3]))
    ritems = [(frag_id + 1,) + i for frag_id, i in enumerate(ritems)]
    output = dcp.OutputWriter("output.gff.bak")
    cwriter = fr.FASTAWriter("ocodon.fasta.bak")
    awriter = fr.FASTAWriter("oamino.fasta.bak")

    for i in ritems:
        output.write_item(
            i[1],
            "dna",
            dcp.ProfileID(i[4], i[5]),
            "dna",
            i[2],
            i[3],
            0,
            {"Epsilon": 0.01},
        )
        cwriter.write_item(f"item{i[0]}", i[6])
        awriter.write_item(f"item{i[0]}", i[7])
    output.close()
    cwriter.close()
    awriter.close()
