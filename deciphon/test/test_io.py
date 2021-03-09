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


def test_scan_minifam(tmp_path: Path, minifam):
    os.chdir(tmp_path)
    filepath = minifam["hmm"]
    shutil.copy(filepath, filepath.name)
    dcp.press(filepath.name)
    filename = bytes(Path(filepath.name).with_suffix(".deciphon"))
    for i, prof in enumerate(dcp.Input.create(filename)):
        alt = prof.models[0]
        # null = prof.models[1]

        multiple_hits = True
        hmmer3_compat = False
        for tgt in minifam["targets"]:
            tmp = minifam["desired"]
            tmp2 = (d for d in tmp if d["defline"] == tgt.defline and d["profid"] == i)
            desired = next(tmp2)
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
            assert_allclose(loglik, float(desired["loglik"]))
            assert str(result.path) == desired["path"]


def test_scan_pfam24_AE014075(tmp_path: Path, pfam24):
    os.chdir(tmp_path)

    tmp = pfam24["desired"]
    desired = {(d["profile"], d["target"]): d["loglik"] for d in tmp}

    filepath = pfam24["hmm"]
    shutil.copy(filepath, filepath.name)
    dcp.press(filepath.name)
    filename = bytes(Path(filepath.name).with_suffix(".deciphon"))

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
            if key in desired:
                assert_allclose(loglik, float(desired[key]))
