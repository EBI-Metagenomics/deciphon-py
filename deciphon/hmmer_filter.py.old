from io import StringIO

import fasta_reader as fr
import gff_io
from hmmer import HMMER


def hmmer_filter(db_filepath):
    hmmer = HMMER(db_filepath)
    hmmer.timeout = 60
    if not hmmer.is_indexed:
        hmmer.index()

    heuristic = True
    cut_ga = True

    targets = fr.read_fasta("oamino.fasta.bak").read_items()
    for i, tgt in enumerate(targets):
        assert tgt.id == f"item{i+1}"
    gffs = gff_io.read_gff("output.gff.bak").read_items()

    acc_targets = {}
    for gff in gffs:
        di = gff.attributes_asdict()
        acc = di["Profile_acc"]
        if acc not in acc_targets:
            acc_targets[acc] = []
        j = int(di["ID"][4:]) - 1
        acc_targets[acc].append(targets[j])

    scores = {}
    for acc, tgts in acc_targets.items():
        txt = [">" + t.defline + "\n" + t.sequence for t in tgts]
        result = hmmer.search(
            StringIO("\n".join(txt)),
            "/dev/null",
            tblout=True,
            heuristic=heuristic,
            cut_ga=cut_ga,
            hmmkey=acc,
            Z=1,
        )
        for row in result.tbl:
            e_value = row.full_sequence.e_value
            score = row.full_sequence.score
            if score.lower() == "nan":
                continue
            bias = row.full_sequence.bias
            itemid = row.target.name
            scores[itemid] = (e_value, score, bias)

    itemid_convert = {}
    j = 1
    with open("output.gff", "w") as out2:
        out2.write("##gff-version 3\n")
        for gff in gffs:
            di = gff.attributes_asdict()
            score = scores.get(di["ID"], None)
            if score is None:
                continue
            itemid_convert[di["ID"]] = f"item{j}"
            attrs = gff.attributes.replace(di["ID"], f"item{j}")
            cols = [
                gff.seqid,
                gff.source,
                gff.type,
                str(gff.start),
                str(gff.end),
                str(gff.score),
                gff.strand,
                str(gff.phase),
                attrs + f";Bias={score[2]};E-value={score[0]};Score={score[1]}",
            ]
            out2.write("\t".join(cols))
            out2.write("\n")
            j += 1

    with fr.write_fasta("oamino.fasta") as f:
        for tgt in targets:
            if tgt.defline not in itemid_convert:
                continue
            f.write_item(itemid_convert[tgt.defline], tgt.sequence)

    ctargets = fr.read_fasta("ocodon.fasta.bak").read_items()
    for i, tgt in enumerate(ctargets):
        assert tgt.id == f"item{i+1}"

    with fr.write_fasta("ocodon.fasta") as f:
        for tgt in ctargets:
            if tgt.defline not in itemid_convert:
                continue
            f.write_item(itemid_convert[tgt.defline], tgt.sequence)
