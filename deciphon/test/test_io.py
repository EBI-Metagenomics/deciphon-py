import os
import shutil
from pathlib import Path

import imm
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

    # desired = minifam["desired"]

    filepath = minifam["hmm"]
    shutil.copy(filepath, filepath.name)
    dcp.press(filepath.name)
    filename = Path(filepath.name).with_suffix(".dcp")

    # multiple_hits = True
    # hmmer3_compat = False
    server = dcp.Server(filename)
    for tgt in minifam["targets"]:
        alt_logliks = server.scan(tgt.sequence.encode())
        del alt_logliks


def test_scan_minifam(tmp_path: Path, minifam):
    os.chdir(tmp_path)

    desired = minifam["desired"]

    filepath = minifam["hmm"]
    shutil.copy(filepath, filepath.name)
    dcp.press(filepath.name)
    filename = bytes(Path(filepath.name).with_suffix(".dcp"))
    for prof in dcp.Input.create(filename):
        prof_acc = prof.metadata.acc.decode()
        alt = prof.models[0]
        # null = prof.models[1]

        multiple_hits = True
        hmmer3_compat = False
        for tgt in minifam["targets"]:
            seq = imm.Sequence.create(tgt.sequence.encode(), alt.hmm.alphabet)
            dp_task = imm.DPTask.create(alt.dp)
            dp_task.setup(seq)
            target_length = len(seq)
            dcp.lib.dcp_profile_setup(
                alt.hmm.imm_hmm,
                alt.dp.imm_dp,
                multiple_hits,
                target_length,
                hmmer3_compat,
            )
            result = alt.dp.viterbi(dp_task)
            loglik = alt.hmm.loglikelihood(seq, result.path)
            key = (prof_acc, tgt.id)
            assert_allclose(loglik, desired[key]["loglik"])


def test_scan_pfam24_AE014075(tmp_path: Path, pfam24):
    os.chdir(tmp_path)

    desired = pfam24["desired"]

    filepath = pfam24["hmm"]
    shutil.copy(filepath, filepath.name)
    dcp.press(filepath.name)
    filename = bytes(Path(filepath.name).with_suffix(".dcp"))

    for prof in dcp.Input.create(filename):
        prof_acc = prof.metadata.acc.decode()
        alt = prof.models[0]

        multiple_hits = True
        hmmer3_compat = False
        for tgt in pfam24["targets"]:
            seq = imm.Sequence.create(tgt.sequence.encode(), alt.hmm.alphabet)
            dp_task = imm.DPTask.create(alt.dp)
            dp_task.setup(seq)
            target_length = len(seq)
            dcp.lib.dcp_profile_setup(
                alt.hmm.imm_hmm,
                alt.dp.imm_dp,
                multiple_hits,
                target_length,
                hmmer3_compat,
            )
            result = alt.dp.viterbi(dp_task)
            loglik = alt.hmm.loglikelihood(seq, result.path)
            key = (prof_acc, tgt.id)
            assert_allclose(loglik, desired[key]["loglik"])
