from __future__ import annotations

from math import log
from typing import List, Type, Union

from imm import MuteState, Sequence, lprob_add, lprob_zero
from nmm import (
    AminoAlphabet,
    AminoLprob,
    BaseLprob,
    CodonLprob,
    CodonMarg,
    DNAAlphabet,
    FrameState,
    RNAAlphabet,
    codon_iter,
)

from .codon_table import CodonTable
from .hmmer_model import HMMERModel
from .model import AltModel, EntryDistr, Node, NullModel, SpecialNode, Transitions
from .profile import Profile, ProfileID

__all__ = ["ProteinProfile", "create_profile"]


class ProteinProfile(Profile):
    @classmethod
    def create(
        cls: Type[ProteinProfile],
        profid: ProfileID,
        factory: ProteinStateFactory,
        null_aminot: AminoLprob,
        core_nodes: List[Node],
        core_trans: List[Transitions],
        entry_distr: EntryDistr,
    ) -> ProteinProfile:

        base_alphabet = factory.genetic_code.base_alphabet

        R = factory.create(b"R", null_aminot)
        null_model = NullModel.create(R)

        special_node = SpecialNode(
            S=MuteState.create(b"S", base_alphabet),
            N=factory.create(b"N", null_aminot),
            B=MuteState.create(b"B", base_alphabet),
            E=MuteState.create(b"E", base_alphabet),
            J=factory.create(b"J", null_aminot),
            C=factory.create(b"C", null_aminot),
            T=MuteState.create(b"T", base_alphabet),
        )

        alt_model = AltModel.create(
            special_node,
            core_nodes,
            core_trans,
            entry_distr,
        )
        # alt_model.set_fragment_length(self._special_transitions)
        return cls(profid, base_alphabet, null_model, alt_model, False)

    # @property
    # def epsilon(self) -> float:
    #     nodes = self._alt_model.core_nodes()
    #     return nodes[0].M.epsilon

    # @classmethod
    # def create_from_binary(
    #     cls: Type[ProteinProfile],
    #     profid: ProfileID,
    #     null_model: nmm.Model,
    #     alt_model: nmm.Model,
    # ):
    #     special_node = wrap.special_node(alt_model.hmm)
    #     core_nodes = wrap.core_nodes(alt_model.hmm)
    #     alt = AltModel.create_from_hmm(
    #         special_node, core_nodes, alt_model.hmm, alt_model.dp
    #     )
    #     null = NullModel.create_from_hmm(null_model.hmm)
    #     return cls(profid, alt_model.hmm.alphabet, null, alt, False)

    # @property
    # def window_length(self) -> int:
    #     return super().window_length

    # @window_length.setter
    # def window_length(self, length: int) -> None:
    #     if length < -1:
    #         raise ValueError("Length must be greater than or equal to -1.")

    #     if length == -1:
    #         length = 2 * 3 * self._alt_model.core_length
    #     self._window_length = length

    def create_sequence(self, sequence: bytes) -> Sequence:
        return Sequence.create(sequence, self.alphabet)

    @property
    def null_model(self) -> NullModel:
        return self._null_model

    @property
    def alt_model(self) -> AltModel:
        return self._alt_model

    # def search(self, sequence: SequenceABC) -> SearchResults:

    #     self._set_target_length_model(len(sequence))
    #     alt_results = self._alt_model.viterbi(sequence, self.window_length)

    #     def create_fragment(
    #         seq: SequenceABC, path: Path, homologous: bool
    #     ):
    #         return ProteinFragment(seq, path, homologous)

    #     search_results = SearchResults(sequence, create_fragment)

    #     for alt_result in alt_results:
    #         subseq = alt_result.sequence
    #         # TODO: temporary fix for reading from binary file
    #         # and consequently alt and null model having different alphabets
    #         s = Sequence.create(bytes(subseq), self._null_model.hmm.alphabet)
    #         viterbi_score0 = self._null_model.loglikelihood(s)
    #         if len(alt_result.path) == 0:
    #             viterbi_score1 = lprob_invalid()
    #         else:
    #             viterbi_score1 = self._alt_model.loglikelihood(alt_result.sequence,
    #                                                            alt_result.path)
    #         score = viterbi_score1 - viterbi_score0
    #         window = Interval(subseq.start, subseq.start + len(subseq))
    #         search_results.append(
    #             score, window, alt_result.path, viterbi_score1, viterbi_score0
    #         )

    #     return search_results


# def create_profile(
#     hmm: HMMERModel,
#     base_abc: Union[RNAAlphabet, DNAAlphabet],
#     window_length: int = 0,
#     epsilon: float = 0.1,
# ) -> ProteinProfile:

#     amino_abc = hmm.alphabet
#     assert isinstance(amino_abc, AminoAlphabet)

#     lprobs = lprob_normalize(hmm.insert_lprobs(0))
#     null_aminot = AminoLprob.create(amino_abc, lprobs)
#     factory = ProteinStateFactory(CodonTable(base_abc, amino_abc), epsilon)

#     nodes: List[Node] = []
#     for m in range(1, hmm.model_length + 1):
#         lprobs = lprob_normalize(hmm.match_lprobs(m))
#         M = factory.create(f"M{m}".encode(), AminoLprob.create(amino_abc, lprobs))

#         lprobs = lprob_normalize(hmm.insert_lprobs(m))
#         I = factory.create(f"I{m}".encode(), AminoLprob.create(amino_abc, lprobs))

#         D = MuteState.create(f"D{m}".encode(), base_abc)

#         nodes.append(Node(M, I, D))

#     trans: List[Transitions] = []
#     for t in hmm.transitions:
#         t.normalize()
#         trans.append(t)

#     profid = ProfileID(hmm.model_id.name, hmm.model_id.acc)
#     prof = ProteinProfile.create(
#         profid, factory, null_aminot, nodes, trans, EntryDistr.UNIFORM
#     )
#     prof.window_length = window_length
#     return prof


def create_profile(
    hmm: HMMERModel,
    base_abc: Union[RNAAlphabet, DNAAlphabet],
    window_length: int = 0,
    epsilon: float = 0.1,
) -> ProteinProfile:

    amino_abc = hmm.alphabet
    assert isinstance(amino_abc, AminoAlphabet)

    null_lprobs = hmm.null_lprobs
    null_log_odds = [0.0] * len(null_lprobs)

    null_aminot = AminoLprob.create(amino_abc, null_lprobs)
    factory = ProteinStateFactory(CodonTable(base_abc, amino_abc), epsilon)

    nodes: List[Node] = []
    for m in range(1, hmm.model_length + 1):
        lodds = [v0 - v1 for v0, v1 in zip(hmm.match_lprobs(m), null_lprobs)]
        M = factory.create(f"M{m}".encode(), AminoLprob.create(amino_abc, lodds))

        I = factory.create(
            f"I{m}".encode(), AminoLprob.create(amino_abc, null_log_odds)
        )

        D = MuteState.create(f"D{m}".encode(), base_abc)

        nodes.append(Node(M, I, D))

    trans = hmm.transitions

    profid = ProfileID(hmm.model_id.name, hmm.model_id.acc)
    entry_distr = EntryDistr.OCCUPANCY
    prof = ProteinProfile.create(
        profid, factory, null_aminot, nodes, trans, entry_distr
    )
    prof.window_length = window_length
    return prof


class ProteinStateFactory:
    def __init__(
        self,
        gcode: CodonTable,
        epsilon: float,
    ):
        self._gcode = gcode
        self._epsilon = epsilon

    def create(self, name: bytes, aminot: AminoLprob) -> FrameState:
        codonp = _create_codon_prob(aminot, self._gcode)
        baset = _create_base_table(codonp)
        codonm = CodonMarg.create(codonp)
        return FrameState.create(name, baset, codonm, self._epsilon)

    @property
    def genetic_code(self) -> CodonTable:
        return self._gcode

    @property
    def epsilon(self) -> float:
        return self._epsilon


def _create_base_table(codonp: CodonLprob):
    base_abc = codonp.alphabet
    base_lprob = {base: lprob_zero() for base in base_abc.symbols}
    norm = log(3)
    for codon in codon_iter(base_abc):
        lprob = codonp.get_lprob(codon)
        triplet = codon.symbols

        base_lprob[triplet[0]] = lprob_add(base_lprob[triplet[0]], lprob - norm)
        base_lprob[triplet[1]] = lprob_add(base_lprob[triplet[1]], lprob - norm)
        base_lprob[triplet[2]] = lprob_add(base_lprob[triplet[2]], lprob - norm)

    assert len(base_lprob) == 4
    bases = base_abc.symbols
    assert len(bases) == 4
    return BaseLprob.create(
        base_abc,
        (
            base_lprob[bases[0]],
            base_lprob[bases[1]],
            base_lprob[bases[2]],
            base_lprob[bases[3]],
        ),
    )


def _create_codon_prob(aminot: AminoLprob, gencode: CodonTable) -> CodonLprob:
    codonp = CodonLprob.create(gencode.base_alphabet)

    codon_lprobs = []
    lprob_norm = lprob_zero()
    for i in range(len(aminot.alphabet.symbols)):
        aa = aminot.alphabet.symbols[i : i + 1]
        lprob = aminot.lprob(aa)

        codons = gencode.codons(aa)
        if len(codons) == 0:
            continue

        norm = log(len(codons))
        for codon in codons:
            codon_lprobs.append((codon, lprob - norm))
            lprob_norm = lprob_add(lprob_norm, codon_lprobs[-1][1])

    for codon, lprob in codon_lprobs:
        codonp.set_lprob(codon, lprob - lprob_norm)

    return codonp
