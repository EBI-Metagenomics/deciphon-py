import deciphon as dcp
import os
import shutil
from pathlib import Path


def test_io(tmp_path: Path):
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
