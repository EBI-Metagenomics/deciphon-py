from __future__ import annotations

from dataclasses import dataclass

from . import lprob

# from enum import Enum
# from math import log
# from typing import Dict, List, Optional, Tuple, Type


# __all__ = [
#     "AltModel",
#     "EntryDistr",
#     "Node",
#     "NullModel",
#     "SpecialNode",
#     "SpecialTransitions",
#     "Transitions",
# ]

LPROB_ZERO = lprob.zero()


# class EntryDistr(Enum):
#     UNIFORM = 1
#     OCCUPANCY = 2


@dataclass
class Transitions:
    MM: float = LPROB_ZERO
    MI: float = LPROB_ZERO
    MD: float = LPROB_ZERO
    IM: float = LPROB_ZERO
    II: float = LPROB_ZERO
    DM: float = LPROB_ZERO
    DD: float = LPROB_ZERO

    def normalize(self):
        m_norm: float = lprob.add(lprob.add(self.MM, self.MI), self.MD)
        self.MM -= m_norm
        self.MI -= m_norm
        self.MD -= m_norm

        i_norm: float = lprob.add(self.IM, self.II)
        self.IM -= i_norm
        self.II -= i_norm

        d_norm: float = lprob.add(self.DM, self.DD)
        self.DM -= d_norm
        self.DD -= d_norm


# @dataclass
# class SpecialTransitions:
#     NN: float = 0.0
#     NB: float = 0.0
#     EC: float = 0.0
#     CC: float = 0.0
#     CT: float = 0.0
#     EJ: float = 0.0
#     JJ: float = 0.0
#     JB: float = 0.0
#     RR: float = 0.0
#     BM: float = 0.0
#     ME: float = 0.0


# class Node:
#     def __init__(self, M: State, I: State, D: MuteState):
#         self._M = M
#         self._I = I
#         self._D = D

#     @property
#     def M(self) -> State:
#         return self._M

#     @property
#     def I(self) -> State:
#         return self._I

#     @property
#     def D(self) -> MuteState:
#         return self._D

#     def states(self) -> List[State]:
#         return [self._M, self._I, self._D]


# class SpecialNode:
#     def __init__(
#         self,
#         S: MuteState,
#         N: State,
#         B: MuteState,
#         E: MuteState,
#         J: State,
#         C: State,
#         T: MuteState,
#     ):
#         self._S = S
#         self._N = N
#         self._B = B
#         self._E = E
#         self._J = J
#         self._C = C
#         self._T = T

#     @property
#     def S(self) -> MuteState:
#         return self._S

#     @property
#     def N(self) -> State:
#         return self._N

#     @property
#     def B(self) -> MuteState:
#         return self._B

#     @property
#     def E(self) -> MuteState:
#         return self._E

#     @property
#     def J(self) -> State:
#         return self._J

#     @property
#     def C(self) -> State:
#         return self._C

#     @property
#     def T(self) -> MuteState:
#         return self._T

#     def states(self) -> List[State]:
#         return [self._S, self._N, self._B, self._E, self._J, self._C, self._T]


# class NullModel:
#     def __init__(self, hmm: HMM, state: State):
#         self._hmm = hmm
#         self._state = state

#     @classmethod
#     def create(cls: Type[NullModel], state: State) -> NullModel:
#         hmm = HMM.create(state.alphabet)
#         hmm.add_state(state, 0.0)
#         return cls(hmm, state)

#     @classmethod
#     def create_from_hmm(cls: Type[NullModel], hmm: HMM) -> NullModel:
#         states = hmm.states()
#         if len(states) != 1:
#             raise ValueError("Null HMM must have only one state.")
#         return cls(hmm, list(states.values())[0])

#     @property
#     def hmm(self) -> HMM:
#         return self._hmm

#     @property
#     def state(self) -> State:
#         return self._state

#     def set_transition(self, lprob: float):
#         self._hmm.set_transition(self.state, self.state, lprob)

#     def loglikelihood(self, sequence: Sequence):
#         steps = [Step.create(self.state, 1) for _ in range(len(sequence))]
#         path = Path.create(steps)
#         return self._hmm.loglikelihood(sequence, path)

#     def set_special_transitions(self, special_trans: SpecialTransitions):
#         self.set_transition(special_trans.RR)

#     def __str__(self):
#         return f"{self._hmm}"


# class AltModel:
#     def __init__(
#         self,
#         special_node: SpecialNode,
#         core_nodes: List[Node],
#         states: Dict[CData, State],
#         hmm: HMM,
#         dp: Optional[DP] = None,
#     ):
#         self._special_node = special_node
#         self._core_nodes = core_nodes
#         self._states: Dict[CData, State] = states
#         self._hmm = hmm
#         self._dp: Optional[DP] = dp
#         self._dp_task: Optional[DPTask] = None

#     @classmethod
#     def create(
#         cls: Type[AltModel],
#         special_node: SpecialNode,
#         core_nodes: List[Node],
#         core_trans: List[Transitions],
#         entry_distr: EntryDistr,
#     ) -> AltModel:

#         states: Dict[CData, State] = {}

#         for node in core_nodes:
#             for state in node.states():
#                 states[state.imm_state] = state

#         for state in special_node.states():
#             states[state.imm_state] = state

#         hmm = HMM.create(special_node.S.alphabet)
#         hmm.add_state(special_node.S, 0.0)
#         hmm.add_state(special_node.N)
#         hmm.add_state(special_node.B)
#         hmm.add_state(special_node.E)
#         hmm.add_state(special_node.J)
#         hmm.add_state(special_node.C)
#         hmm.add_state(special_node.T)

#         for node in core_nodes:
#             hmm.add_state(node.M)
#             hmm.add_state(node.I)
#             hmm.add_state(node.D)

#         M1 = core_nodes[0].M
#         hmm.set_transition(special_node.B, M1, core_trans[0].MM)

#         for i, trans in enumerate(core_trans[1:-1]):
#             prev = core_nodes[i]
#             next = core_nodes[i + 1]
#             hmm.set_transition(prev.M, prev.I, trans.MI)
#             hmm.set_transition(prev.I, prev.I, trans.II)
#             hmm.set_transition(prev.M, next.M, trans.MM)
#             hmm.set_transition(prev.I, next.M, trans.IM)
#             hmm.set_transition(prev.M, next.D, trans.MD)
#             hmm.set_transition(prev.D, next.D, trans.DD)
#             hmm.set_transition(prev.D, next.M, trans.DM)

#         Mm = core_nodes[-1].M
#         hmm.set_transition(Mm, special_node.E, core_trans[-1].MM)

#         alt_model = cls(special_node, core_nodes, states, hmm)

#         alt_model.set_entry_transitions(entry_distr, core_trans)
#         alt_model.set_exit_transitions()

#         return alt_model

#     @classmethod
#     def create_from_hmm(
#         cls: Type[AltModel],
#         special_node: SpecialNode,
#         core_nodes: List[Node],
#         hmm: HMM,
#         dp: DP,
#     ) -> AltModel:

#         states: Dict[CData, State] = {}

#         for node in core_nodes:
#             for state in node.states():
#                 states[state.imm_state] = state

#         for state in special_node.states():
#             states[state.imm_state] = state

#         alt_model = cls(special_node, core_nodes, states, hmm, dp)

#         # alt_model.set_entry_transitions(entry_distr, core_trans)
#         # alt_model.set_exit_transitions()

#         return alt_model

#     @property
#     def hmm(self) -> HMM:
#         return self._hmm

#     def set_transition(self, a: State, b: State, lprob: float):
#         # self._dp = None
#         self._hmm.set_transition(a, b, lprob)

#     def core_nodes(self) -> List[Node]:
#         return self._core_nodes

#     @property
#     def special_node(self) -> SpecialNode:
#         return self._special_node

#     @property
#     def core_length(self) -> int:
#         return len(self._core_nodes)

#     def loglikelihood(self, sequence: Sequence, path: Path) -> float:
#         return self._hmm.loglikelihood(sequence, path)

#     def viterbi(self, seq: Sequence, window_length: int = 0) -> imm.Results:
#         if self._dp is None:
#             self._dp = self._hmm.create_dp(self.special_node.T)

#         if self._dp_task is None:
#             self._dp_task = DPTask.create(self._dp)

#         self._dp_task.setup(seq, window_length)
#         return self._dp.viterbi(self._dp_task)

#     def set_fragment_length(self, special_trans: SpecialTransitions):
#         del self
#         del special_trans
#         raise RuntimeError("Fix this function to update dp.")
#         # M = self.core_length
#         # if M == 0:
#         #     return

#         # self._dp = None
#         # B = self.special_node.B
#         # E = self.special_node.E

#         # # Uniform local alignment fragment length distribution
#         # t = special_trans
#         # t.BM = log(2) - log(M) - log(M + 1)
#         # t.ME = 0.0
#         # for node in self.core_nodes():
#         #     self.set_transition(B, node.M, t.BM)
#         #     self.set_transition(node.M, E, t.ME)

#         # for node in self.core_nodes()[1:]:
#         #     self.set_transition(node.D, E, 0.0)

#     def set_entry_transitions(
#         self, entry_distr: EntryDistr, core_trans: List[Transitions]
#     ):
#         if entry_distr == EntryDistr.UNIFORM:
#             M = self.core_length
#             costs = [log(2.0 / (M * (M + 1)))] * M

#         elif entry_distr == EntryDistr.OCCUPANCY:
#             log_occ, logZ = _calculate_occupancy(core_trans)
#             costs = [locc - logZ for locc in log_occ]
#         else:
#             raise RuntimeError("Unkown entry distribution: {}.".format(entry_distr))

#         B = self.special_node.B
#         for cost, node in zip(costs, self.core_nodes()):
#             self.set_transition(B, node.M, cost)

#     def set_exit_transitions(self):
#         E = self.special_node.E

#         for node in self.core_nodes():
#             self.set_transition(node.M, E, 0.0)

#         for node in self.core_nodes()[1:]:
#             self.set_transition(node.D, E, 0.0)

#     def set_special_transitions(
#         self, special_trans: SpecialTransitions, hmmer3_compat=False
#     ):
#         t = special_trans
#         node = self.special_node
#         if self._dp is not None:
#             if hmmer3_compat:
#                 t.NN = 0.0
#                 t.CC = 0.0
#                 t.JJ = 0.0

#             def dp_set(a, b, lprob):
#                 imm.lib.imm_dp_change_trans(
#                     self._dp.imm_dp,
#                     self._hmm.imm_hmm,
#                     a.imm_state,
#                     b.imm_state,
#                     lprob,
#                 )

#             dp_set(node.S, node.B, t.NB)
#             dp_set(node.S, node.N, t.NN)
#             dp_set(node.N, node.N, t.NN)
#             dp_set(node.N, node.B, t.NB)

#             dp_set(node.E, node.T, t.EC + t.CT)
#             dp_set(node.E, node.C, t.EC + t.CC)
#             dp_set(node.C, node.C, t.CC)
#             dp_set(node.C, node.T, t.CT)

#             dp_set(node.E, node.B, t.EJ + t.JB)
#             dp_set(node.E, node.J, t.EJ + t.JJ)
#             dp_set(node.J, node.J, t.JJ)
#             dp_set(node.J, node.B, t.JB)

#             dp_set(node.B, self._core_nodes[1].D, LPROB_ZERO)
#             dp_set(node.B, self._core_nodes[0].I, LPROB_ZERO)
#         else:
#             self._dp = None

#             if hmmer3_compat:
#                 t.NN = 0.0
#                 t.CC = 0.0
#                 t.JJ = 0.0

#             self.set_transition(node.S, node.B, t.NB)
#             self.set_transition(node.S, node.N, t.NN)
#             self.set_transition(node.N, node.N, t.NN)
#             self.set_transition(node.N, node.B, t.NB)

#             self.set_transition(node.E, node.T, t.EC + t.CT)
#             self.set_transition(node.E, node.C, t.EC + t.CC)
#             self.set_transition(node.C, node.C, t.CC)
#             self.set_transition(node.C, node.T, t.CT)

#             self.set_transition(node.E, node.B, t.EJ + t.JB)
#             self.set_transition(node.E, node.J, t.EJ + t.JJ)
#             self.set_transition(node.J, node.J, t.JJ)
#             self.set_transition(node.J, node.B, t.JB)

#             # TODO: if fails for HMM having one core state
#             self.set_transition(node.B, self._core_nodes[1].D, LPROB_ZERO)
#             self.set_transition(node.B, self._core_nodes[0].I, LPROB_ZERO)

#     def __str__(self):
#         msg = f"{self._hmm}\n"
#         msg += f"DP: {self._dp}"
#         return msg


# def _calculate_occupancy(core_trans: List[Transitions]) -> Tuple[List[float], float]:
#     log_occ = [lprob.add(core_trans[0].MI, core_trans[0].MM)]
#     for trans in core_trans[1:-1]:
#         val0 = log_occ[-1] + lprob.add(trans.MM, trans.MI)
#         val1 = _log1_p(log_occ[-1]) + trans.DM
#         log_occ.append(lprob.add(val0, val1))

#     logZ = LPROB_ZERO
#     for i, locc in enumerate(log_occ):
#         logZ = lprob.add(logZ, locc + log(len(log_occ) - i))

#     return log_occ, logZ


# def _log1_p(log_p: float):
#     """
#     Computes log(1 - p) given log(p).
#     """
#     from math import exp, log1p

#     return log1p(-exp(log_p))
