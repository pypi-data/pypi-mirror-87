# https://github.com/alisoltanirad/Logic.git

class Sentence:

    def __invert__(self):
        return Invert(self)

    def __and__(self, other):
        return Conjunction(self, other)

    def __or__(self, other):
        return Disjunction(self, other)

    def __gt__(self, other):
        return Implication(self, other)

    def __eq__(self, other):
        return Equality(self, other)


class BinarySentence(Sentence):

    def __init__(self, lchild, rchild):
        self.lchild = lchild
        self.rchild = rchild

    def __str__(self):
        return '(' + str(self.lchild) + ' ' + \
               self.operator + \
               ' ' + str(self.rchild) +  ')'


class Atomic(Sentence):

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return str(self.name)

    def __hash__(self):
        return hash(self.name)

    def validate(self, set):
        return self in set


class Invert(Sentence):
    operator = '¬'

    def __init__(self, child):
        self.child = child

    def __str__(self):
        return self.operator + str(self.child)

    def __hash__(self):
        return hash(not self.child)

    def validate(self, set):
        return not self.child in set


class Conjunction(BinarySentence):
    operator = '∧'

    def __hash__(self):
        return hash(self.lchild and self.rchild)

    def validate(self, set):
        return self.lchild.validate(set) and self.rchild.validate(set)


class Disjunction(BinarySentence):
    operator = '∨'

    def __hash__(self):
        return hash(self.lchild or self.rchild)

    def validate(self, set):
        return self.lchild.validate(set) or self.rchild.validate(set)


class Implication(BinarySentence):
    operator = '→'

    def __hash__(self):
        return hash(not self.lchild or self.rchild)

    def validate(self, set):
        return not self.lchild.validate(set) or self.rchild.validate(set)


class Equality(BinarySentence):
    operator = '↔'

    def __hash__(self):
        return hash((self.lchild and self.rchild) or
                    (not self.lchild and not self.rchild))

    def validate(self, set):
        return self.lchild.validate(set) is self.rchild.validate(set)


class SentenceSet:

    def __init__(self, set):
        self.__set = set

    def __str__(self):
        return str(self.__set)

    def parse(self):
        input_set = self.__set.copy()
        parsed_set = set()
        while input_set:
            sentence = input_set.pop()

            if (type(sentence) is Atomic) or (type(sentence) is Invert):
                parsed_set.add(sentence)

            elif type(sentence) is Conjunction:
                input_set.add(sentence.lchild)
                input_set.add(sentence.rchild)

            elif type(sentence) is Disjunction:
                if (~sentence.lchild).validate(input_set | parsed_set):
                    input_set.add(sentence.rchild)
                elif (~sentence.rchild).validate(input_set | parsed_set):
                    input_set.add(sentence.lchild)

            elif type(sentence) is Implication:
                if sentence.lchild.validate(input_set | parsed_set):
                    input_set.add(sentence.rchild)

            elif type(sentence) is Equality:
                if sentence.lchild.validate(input_set | parsed_set):
                    input_set.add(sentence.rchild)
                elif sentence.rchild.validate(input_set | parsed_set):
                    input_set.add(sentence.lchild)
                elif (~sentence.lchild).validate(input_set | parsed_set):
                    input_set.add(~sentence.rchild)
                elif (~sentence.rchild).validate(input_set | parsed_set):
                    input_set.add(~sentence.lchild)

        return parsed_set
