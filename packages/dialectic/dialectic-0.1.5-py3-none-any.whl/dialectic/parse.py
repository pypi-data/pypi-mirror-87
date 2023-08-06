from .sentence import *


def parse(sentence_list):
    input_list = sentence_list.copy()
    parsed_list = []
    while input_list:
        sentence = input_list.pop()

        if (type(sentence) is Atomic) or (type(sentence) is Invert):
            parsed_list.add(sentence)

        elif type(sentence) is Conjunction:
            input_list.add(sentence.lchild)
            input_list.add(sentence.rchild)

        elif type(sentence) is Disjunction:
            if (~sentence.lchild).validate(input_list + parsed_list):
                input_list.add(sentence.rchild)
            elif (~sentence.rchild).validate(input_list + parsed_list):
                input_list.add(sentence.lchild)

        elif type(sentence) is Implication:
            if sentence.lchild.validate(input_list + parsed_list):
                input_list.add(sentence.rchild)

        elif type(sentence) is Equality:
            if sentence.lchild.validate(input_list + parsed_list):
                input_list.add(sentence.rchild)
            elif sentence.rchild.validate(input_list + parsed_list):
                input_list.add(sentence.lchild)
            elif (~sentence.lchild).validate(input_list + parsed_list):
                input_list.add(~sentence.rchild)
            elif (~sentence.rchild).validate(input_list + parsed_list):
                input_list.add(~sentence.lchild)

    return set(parsed_list)