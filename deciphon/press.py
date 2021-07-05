from pathlib import Path
from typing import Union

from hmmer_reader import num_models, open_hmmer
from tqdm import tqdm

# from .dcp_profile import DCPProfile
from .hmmer_model import HMMERModel
from .metadata import Metadata

# from .output import Output
# from .protein_profile import create_profile

__all__ = ["press"]


def press(hmm_filepath: Union[Path, str]):
    hmm_filepath = Path(hmm_filepath)
    # base_abc = nmm.DNAAlphabet()

    total = num_models(hmm_filepath)
    # epsilon = 0.01
    # bin_filepath = hmm_filepath.with_suffix(".dcp").name.encode()

    # with Output.create(bin_filepath) as output:
    with open_hmmer(hmm_filepath) as parser:
        for hmmer3 in tqdm(parser, total=total, desc="Pressing"):
            model = HMMERModel(hmmer3)
            data = dict(hmmer3.metadata)
            mt = Metadata(data["NAME"].encode(), data["ACC"].encode())
            del model
            del mt
            # prof = create_profile(model, base_abc, 0, epsilon)

            # nprof = DCPProfile.create(base_abc, mt)

            # hmm = prof.alt_model.hmm
            # dp = hmm.create_dp(prof.alt_model.special_node.T)
            # nprof.append_model(imm.Model.create(hmm, dp))

            # hmm = prof.null_model.hmm
            # dp = hmm.create_dp(prof.null_model.state)
            # nprof.append_model(imm.Model.create(hmm, dp))

            # output.write(nprof)
