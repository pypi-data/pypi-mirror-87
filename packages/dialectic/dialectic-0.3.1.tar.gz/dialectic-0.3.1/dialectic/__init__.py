from .sentence import (
    Atomic, Invert, Conjunction, Disjunction, Implication, Equality
)
from .parse import parse_sentences
from .inference import Inference, is_contradictory
