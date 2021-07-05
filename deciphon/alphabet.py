# from fasta_reader import FASTAReader
# from hmmer_reader import HMMERParser

__all__ = [
    "infer_alphabet",
    # "infer_fasta_alphabet",
    # "infer_hmmer_alphabet",
    "Alphabet",
    "NucltAlphabet",
    "AminoAlphabet",
    "DNAAlphabet",
    "RNAAlphabet",
    "IUPACAminoAlphabetAlphabet",
    "DNA",
    "RNA",
    "IUPACAmino",
]

dna_symbols = "ACGT"
rna_symbols = "ACGU"
iupac_amino_symbols = "ACDEFGHIKLMNPQRSTVWY"


class Alphabet:
    def __init__(self, symbols: str):
        self._symbols = symbols

    @property
    def symbols(self) -> str:
        return self._symbols


class NucltAlphabet(Alphabet):
    pass


class DNAAlphabet(NucltAlphabet):
    def __init__(self):
        super().__init__("ACGT")


class RNAAlphabet(NucltAlphabet):
    def __init__(self):
        super().__init__("ACGU")


class AminoAlphabet(Alphabet):
    pass


class IUPACAminoAlphabetAlphabet(AminoAlphabet):
    def __init__(self):
        super().__init__("ACDEFGHIKLMNPQRSTVWY")


DNA = DNAAlphabet()
RNA = RNAAlphabet()
IUPACAmino = IUPACAminoAlphabetAlphabet()

# def alphabet_name(alphabet: Alphabets) -> str:
#     if isinstance(alphabet, IUPACAminoAlphabet):
#         return "amino"
#     if isinstance(alphabet, DNAAlphabet):
#         return "dna"
#     if isinstance(alphabet, RNAAlphabet):
#         return "rna"

#     # TODO: it is temporary
#     if isinstance(alphabet, BaseAlphabet):
#         if set(alphabet.symbols) == set(b"ACGT"):
#             return "dna"
#         if set(alphabet.symbols) == set(b"ACGU"):
#             return "rna"
#     raise ValueError("Unknown alphabet.")


def infer_alphabet(sequence: str):
    """
    Infer alphabet from a sequence of symbols.

    Parameters
    ----------
    sequence
        Sequence of symbols.
    """

    symbols = set(sequence)

    if len(symbols - set(DNA.symbols)) == 0:
        return DNA

    if len(symbols - set(RNA.symbols)) == 0:
        return RNA

    if len(symbols - set(IUPACAmino.symbols)) == 0:
        return IUPACAmino

    raise ValueError("Failed to infer alphabet.")


# def infer_fasta_alphabet(parser: FASTAReader) -> Optional[Alphabets]:
#     """
#     Infer alphabet from fasta file.

#     Parameters
#     ----------
#     parser
#         FASTA parser.
#     """

#     for item in parser:
#         alphabet = infer_alphabet(item.sequence.encode())
#         if alphabet is not None:
#             return alphabet

#     return None


# def infer_hmmer_alphabet(parser: HMMERParser) -> Optional[Alphabets]:

#     for prof in parser:
#         alph = dict(prof.metadata)["ALPH"].lower()
#         if alph == "amino":
#             return IUPACAminoAlphabet()
#         if alph == "dna":
#             return DNAAlphabet()
#         if alph == "rna":
#             return RNAAlphabet()

#     return None
