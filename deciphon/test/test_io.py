import os
import shutil
from pathlib import Path
from time import sleep

from imm.testing import assert_allclose

import deciphon as dcp


def test_press(tmp_path: Path):
    os.chdir(tmp_path)
    filepath = dcp.example.get("minifam.hmm")
    filename = filepath.name
    shutil.copy(filepath, filename)
    dcp.press(filename)


def test_scan_minifam_server(tmp_path: Path, minifam):
    os.chdir(tmp_path)

    filepath = minifam["hmm"]
    shutil.copy(filepath, filepath.name)
    dcp.press(filepath.name)
    filename = Path(filepath.name).with_suffix(".dcp")

    desired = minifam["desired"]
    for multiple_hits in [True, False]:
        for hmmer3_compat in [True, False]:

            task = dcp.Task(True, True, multiple_hits, hmmer3_compat)
            tgt_id = []
            for tgt in minifam["targets"]:
                task.add_seq(tgt.sequence.encode())
                tgt_id.append(tgt.id)

            server = dcp.Server(filename)
            server.start()
            server.add_task(task)
            while not task.end():
                r = task.read()
                if r is not None:
                    target = tgt_id[r.seqid]
                    profile = server.metadata(r.profid).acc
                    key = (multiple_hits, hmmer3_compat, target, profile)
                    assert_allclose(desired[key]["alt_loglik"], r.alt_loglik)
                    assert_allclose(desired[key]["null_loglik"], r.null_loglik)
                    assert desired[key]["alt_path"] == r.alt_stream
                    assert desired[key]["null_path"] == r.null_stream
                    assert desired[key]["alt_codon_stream"] == r.alt_codon_stream
                    assert desired[key]["null_codon_stream"] == r.null_codon_stream
                    assert desired[key]["alt_amino_stream"] == r.alt_amino_stream
                    assert desired[key]["null_amino_stream"] == r.null_amino_stream
                    server.free_result(r)
                sleep(0.01)
            if task.end():
                server.free_task(task)
            server.stop()
            server.join()


def test_scan_pfam24_server(tmp_path: Path, pfam24):
    # print(r.profid, r.seqid, r.null_loglik, r.alt_loglik)
    os.chdir(tmp_path)

    filepath = pfam24["hmm"]
    shutil.copy(filepath, filepath.name)
    dcp.press(filepath.name)
    filename = Path(filepath.name).with_suffix(".dcp")

    # print("[")
    desired = pfam24["desired"]
    for multiple_hits in [True, False]:
        for hmmer3_compat in [True, False]:

            task = dcp.Task(True, True, multiple_hits, hmmer3_compat)
            tgt_id = []
            for tgt in pfam24["targets"]:
                task.add(tgt.sequence.encode())
                tgt_id.append(tgt.id)

            server = dcp.Server(filename)
            server.scan(task)
            task_result = task.result
            for r in task_result.results:
                # print("{")
                # print(f"\"multiple_hits\": {str(multiple_hits).lower()},")
                # print(f"\"hmmer3_compat\": {str(hmmer3_compat).lower()},")
                # print(f"\"target\": \"{tgt_id[r.seqid]}\",")
                # print(f"\"profile\": \"{server.metadata(r.profid).acc}\",")
                # print(f"\"alt_loglik\": {r.alt_loglik},")
                # print(f"\"alt_path\": \"{r.alt_stream}\",")
                # print(f"\"alt_codon_stream\": \"{r.alt_codon_stream}\",")
                # print(f"\"alt_amino_stream\": \"{r.alt_amino_stream}\",")
                # print(f"\"null_loglik\": {r.null_loglik},")
                # print(f"\"null_path\": \"{r.null_stream}\",")
                # print(f"\"null_codon_stream\": \"{r.null_codon_stream}\",")
                # print(f"\"null_amino_stream\": \"{r.null_amino_stream}\"")
                # print("},")
                target = tgt_id[r.seqid]
                profile = server.metadata(r.profid).acc
                key = (multiple_hits, hmmer3_compat, target, profile)
                assert_allclose(desired[key]["alt_loglik"], r.alt_loglik)
                assert_allclose(desired[key]["null_loglik"], r.null_loglik)
                assert desired[key]["alt_path"] == r.alt_stream
                assert desired[key]["null_path"] == r.null_stream
                assert desired[key]["alt_codon_stream"] == r.alt_codon_stream
                assert desired[key]["null_codon_stream"] == r.null_codon_stream
                assert desired[key]["alt_amino_stream"] == r.alt_amino_stream
                assert desired[key]["null_amino_stream"] == r.null_amino_stream
    # print("]")
