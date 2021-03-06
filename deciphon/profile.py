from abc import ABC, abstractmethod
from math import log
from typing import NamedTuple

from imm import Alphabet, Sequence, lprob_zero

from .model import AltModel, NullModel, SpecialTransitions

__all__ = ["Profile", "ProfileID"]

ProfileID = NamedTuple("ProfileID", [("name", str), ("acc", str)])


class Profile(ABC):
    def __init__(
        self,
        profid: ProfileID,
        alphabet: Alphabet,
        null_model: NullModel,
        alt_model: AltModel,
        hmmer3_compat: bool,
    ):
        self._profid = profid
        self._alphabet = alphabet
        self._null_model = null_model
        self._alt_model = alt_model
        self._multiple_hits: bool = True
        self._special_trans = SpecialTransitions()
        self._hmmer3_compat = hmmer3_compat
        self._set_target_length_model(1)

    @property
    def profid(self) -> ProfileID:
        return self._profid

    @property
    def alphabet(self):
        return self._alphabet

    @abstractmethod
    def create_sequence(self, sequence: bytes) -> Sequence:
        del self
        del sequence
        raise NotImplementedError()

    @property
    def null_model(self) -> NullModel:
        del self
        raise NotImplementedError()

    @property
    def alt_model(self) -> AltModel:
        del self
        raise NotImplementedError()

    @property
    def multiple_hits(self) -> bool:
        return self._multiple_hits

    @multiple_hits.setter
    def multiple_hits(self, multiple_hits: bool):
        self._multiple_hits = multiple_hits

    def _set_target_length_model(self, target_length: int):
        t = self._get_target_length_model(target_length)
        self._null_model.set_special_transitions(t)
        self._alt_model.set_special_transitions(t, self._hmmer3_compat)

    def _get_target_length_model(self, target_length: int) -> SpecialTransitions:
        L = target_length
        if L == 0:
            raise ValueError("Target length cannot be zero.")

        if self._multiple_hits:
            q = 0.5
            log_q = log(0.5)
        else:
            q = 0.0
            log_q = lprob_zero()

        lp = log(L) - log(L + 2 + q / (1 - q))
        l1p = log(2 + q / (1 - q)) - log(L + 2 + q / (1 - q))
        lr = log(L) - log(L + 1)

        t = self._special_trans

        t.NN = t.CC = t.JJ = lp
        t.NB = t.CT = t.JB = l1p
        t.RR = lr
        t.EJ = log_q
        t.EC = log(1 - q)

        return t
