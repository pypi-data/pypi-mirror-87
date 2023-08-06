from .sentence import Disjunction
from .parse import parse_sentences


class Inference:

    def __init__(self, conclusion, premises=[]):
        self.conclusion = conclusion
        self.parsed_conclusion = parse_sentences([self.conclusion])
        self.parsed_premises = parse_sentences(premises)

    def is_valid_argument(self):
        return self.conclusion.validate(set(self.parsed_premises))

    def is_tautology(self):
        if type(self.conclusion) is Disjunction:
            if self.conclusion.lchild.validate(set(~self.conclusion.rchild)):
                return True
        return False

    def is_contradictory(self):
        return is_contradictory(self.parsed_conclusion)

    def is_contingent(self):
        return not (self.is_tautology() or self.is_contradictory())


def is_contradictory(sentence_list):
    parsed_sentences = parse_sentences(sentence_list)
    for sentence in parsed_sentences:
        if ~sentence in parsed_sentences:
            return True
    return False
