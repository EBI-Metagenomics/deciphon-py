import os
import shutil
from pathlib import Path

import imm

import deciphon as dcp


def test_press(tmp_path: Path):
    os.chdir(tmp_path)
    filepath = dcp.example.get("minifam.hmm")
    filename = filepath.name
    shutil.copy(filepath, filename)
    dcp.press(filename)


def test_scan(tmp_path: Path, minifam_consensus, minifam_desired):
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
        for tgt in minifam_consensus:
            tmp = minifam_desired
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
