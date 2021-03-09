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
    desired_loglikgs = [
        [-538.134521484375, -747.7845458984375, -762.9783935546875],
        [-1067.360107421875, -792.2489624023438, -1089.6944580078125],
        [-713.920654296875, -714.9746704101562, -480.3268737792969],
    ]
    server = dcp.Server(filename)
    for i, tgt in enumerate(minifam["targets"]):
        alt_logliks, profids = server.scan(tgt.sequence.encode())
        lista = zip(alt_logliks, profids)
        alt_logliks = [v[0] for v in sorted(lista, key=lambda j: j[1])]
        assert_allclose(alt_logliks, desired_loglikgs[i])


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
