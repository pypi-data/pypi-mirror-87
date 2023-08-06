from .sentence import *


def parse(sentence_list):
    input_set = sentence_list.copy()
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