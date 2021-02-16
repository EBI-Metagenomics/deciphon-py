from pathlib import Path

from hmmer_reader import num_models, open_hmmer
from imm import HMMBlock
from nmm import DNAAlphabet, Model
from ._output import Output
from tqdm import tqdm

from .hmmer_model import HMMERModel
from .protein_profile import create_profile

__all__ = ["press"]


def press(hmm_filepath: Path):
    base_abc = DNAAlphabet()

    total = num_models(hmm_filepath)
    epsilon = 0.01
    bin_filepath = hmm_filepath.with_suffix(".deciphon").name.encode()

    with Output.create(bin_filepath, total) as output:
        with open_hmmer(hmm_filepath) as parser:
            for plain_model in tqdm(parser, total=total, desc="Pressing"):
                model = HMMERModel(plain_model)
                prof = create_profile(model, base_abc, 0, epsilon)

                hmm = prof.alt_model.hmm
                dp = hmm.create_dp(prof.alt_model.special_node.T)
                model = Model.create(hmm.alphabet)
                model.append_hmm_block(HMMBlock.create(hmm, dp))

                hmm = prof.null_model.hmm
                dp = hmm.create_dp(prof.null_model.state)
                model.append_hmm_block(HMMBlock.create(hmm, dp))
                output.write(model)
                # nfile.write(Model.create(hmm, dp))
                # name = model.model_id.name
                # acc = model.model_id.acc
                # mfile.write(f"{name}\t{acc}\n")
