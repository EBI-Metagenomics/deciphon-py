import deciphon as dcp
import os
import shutil
from pathlib import Path


def test_press(tmp_path: Path):
    os.chdir(tmp_path)
    filepath = dcp.example.get("minifam.hmm")
    filename = filepath.name
    shutil.copy(filepath, filename)
    dcp.press(filename)

    # with open("consensus.fasta", "w") as file:
    #     file.write(_consensus)

    # with open("desired_output.gff", "w") as file:
    #     file.write(_desired_output)

    # with open("desired_ocodon.fasta", "w") as file:
    #     file.write(_desired_ocodon)

    # with open("desired_oamino.fasta", "w") as file:
    #     file.write(_desired_oamino)

    # r = invoke(cli, ["pscan3", str(profile), "consensus.fasta"])
    # assert r.exit_code == 0, r.output

    # oamino = "desired_oamino.fasta"
    # assert_that(contents_of("oamino.fasta")).is_equal_to(contents_of(oamino))
    # ocodon = "desired_ocodon.fasta"
    # assert_that(contents_of("ocodon.fasta")).is_equal_to(contents_of(ocodon))
    # output = "desired_output.gff"
    # assert_that(contents_of("output.gff")).is_equal_to(contents_of(output))


_consensus = """>Homoserine_dh-consensus
CCTATCATTTCGACGCTCAAGGAGTCGCTGACAGGTGACCGTATTACTCGAATCGAAGGG
ATATTAAACGGCACCCTGAATTACATTCTCACTGAGATGGAGGAAGAGGGGGCTTCATTC
TCTGAGGCGCTGAAGGAGGCACAGGAATTGGGCTACGCGGAAGCGGATCCTACGGACGAT
GTGGAAGGGCTAGATGCTGCTAGAAAGCTGGCAATTCTAGCCAGATTGGCATTTGGGTTA
GAGGTCGAGTTGGAGGACGTAGAGGTGGAAGGAATTGAAAAGCTGACTGCCGAAGATATT
GAAGAAGCGAAGGAAGAGGGTAAAGTTTTAAAACTAGTGGCAAGCGCCGTCGAAGCCAGG
GTCAAGCCTGAGCTGGTACCTAAGTCACATCCATTAGCCTCGGTAAAAGGCTCTGACAAC
GCCGTGGCTGTAGAAACGGAACGGGTAGGCGAACTCGTAGTGCAGGGACCAGGGGCTGGC
GCAGAGCCAACCGCATCCGCTGTACTCGCTGACCTTCTC
>AA_kinase-consensus
AAACGTGTAGTTGTAAAGCTTGGGGGTAGTTCTCTGACAGATAAGGAAGAGGCATCACTC
AGGCGTTTAGCTGAGCAGATTGCAGCATTAAAAGAGAGTGGCAATAAACTAGTGGTCGTG
CATGGAGGCGGCAGCTTCACTGATGGTCTGCTGGCATTGAAAAGTGGCCTGAGCTCGGGC
GAATTAGCTGCGGGGTTGAGGAGCACGTTAGAAGAGGCCGGAGAAGTAGCGACGAGGGAC
GCCCTAGCTAGCTTAGGGGAACGGCTTGTTGCAGCGCTGCTGGCGGCGGGTCTCCCTGCT
GTAGGACTCAGCGCCGCTGCGTTAGATGCGACGGAGGCGGGCCGGGATGAAGGCAGCGAC
GGGAACGTCGAGTCCGTGGACGCAGAAGCAATTGAGGAGTTGCTTGAGGCCGGGGTGGTC
CCCGTCCTAACAGGATTTATCGGCTTAGACGAAGAAGGGGAACTGGGAAGGGGATCTTCT
GACACCATCGCTGCGTTACTCGCTGAAGCTTTAGGCGCGGACAAACTCATAATACTGACC
GACGTAGACGGCGTTTACGATGCCGACCCTAAAAAGGTCCCAGACGCGAGGCTCTTGCCA
GAGATAAGTGTGGACGAGGCCGAGGAAAGCGCCTCCGAATTAGCGACCGGTGGGATGAAG
GTCAAACATCCAGCGGCTCTTGCTGCAGCTAGACGGGGGGGTATTCCGGTCGTGATAACG
AAT
>23ISL-consensus
CAGGGTCTGGATAACGCTAATCGTTCGCTAGTTCGCGCTACAAAAGCAGAAAGTTCAGAT
ATACGGAAAGAGGTGACTAACGGCATCGCTAAAGGGCTGAAGCTAGACAGTCTGGAAACA
GCTGCAGAGTCGAAGAACTGCTCAAGCGCACAGAAAGGCGGATCGCTAGCTTGGGCAACC
AACTCCCAACCACAGCCTCTCCGTGAAAGTAAGCTTGAGCCATTGGAAGACTCCCCACGT
AAGGCTTTAAAAACACCTGTGTTGCAAAAGACATCCAGTACCATAACTTTACAAGCAGTC
AAGGTTCAACCTGAACCCCGCGCTCCCGTCTCCGGGGCGCTGTCCCCGAGCGGGGAGGAA
CGCAAGCGCCCAGCTGCGTCTGCTCCCGCTACCTTACCGACACGACAGAGTGGTCTAGGT
TCTCAGGAAGTCGTTTCGAAGGTGGCGACTCGCAAAATTCCAATGGAGTCACAACGCGAG
TCGACT
"""


def test_scan(tmp_path: Path, minifam_desired):
    from io import StringIO
    import deciphon as dcp
    import fasta_reader as fr
    import imm
    from imm.testing import assert_allclose

    os.chdir(tmp_path)
    filepath = dcp.example.get("minifam.hmm")
    shutil.copy(filepath, filepath.name)
    dcp.press(filepath.name)
    filename = bytes(Path(filepath.name).with_suffix(".deciphon"))
    for i, prof in enumerate(dcp.Input.create(filename)):
        alt = prof.models[0]
        # null = prof.models[1]

        multiple_hits = True
        hmmer3_compat = False
        for tgt in fr.read_fasta(StringIO(_consensus)):
            tmp = minifam_desired
            tmp2 = (d for d in tmp if d["defline"] == tgt.defline and d["profid"] == i)
            desired = next(tmp2)
            seq = imm.Sequence.create(tgt.sequence.encode(), alt.hmm.alphabet)
            dp_task = imm.DPTask.create(alt.dp)
            dp_task.setup(seq)
            target_length = len(seq)
            dcp.lib.dcp_profile_setup(alt.hmm.imm_hmm, alt.dp.imm_dp,
                                      multiple_hits, target_length, hmmer3_compat)
            result = alt.dp.viterbi(dp_task)
            loglik = alt.hmm.loglikelihood(seq, result.path)
            assert_allclose(loglik, float(desired["loglik"]))
            assert str(result.path) == desired["path"]
