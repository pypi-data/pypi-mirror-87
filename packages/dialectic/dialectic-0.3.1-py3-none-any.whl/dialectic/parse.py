from .sentence import *


def parse_sentences(sentence_list):
    input_list = sentence_list.copy()
    parsed_list = []
    while input_list:
        sentence = input_list.pop()

        if (type(sentence) is Atomic):
            parsed_list.append(sentence)

        if (type(sentence) is Invert):
            parsed_list.append(sentence)

        elif type(sentence) is Conjunction:
            input_list.append(sentence.lchild)
            input_list.append(sentence.rchild)

        elif type(sentence) is Disjunction:
            if (~sentence.lchild).validate(set(input_list + parsed_list)):
                input_list.append(sentence.rchild)
            elif (~sentence.rchild).validate(set(input_list + parsed_list)):
                input_list.append(sentence.lchild)

        elif type(sentence) is Implication:
            if sentence.lchild.validate(set(input_list + parsed_list)):
                input_list.append(sentence.rchild)

        elif type(sentence) is Equality:
            if sentence.lchild.validate(set(input_list + parsed_list)):
                input_list.append(sentence.rchild)
            elif sentence.rchild.validate(set(input_list + parsed_list)):
                input_list.append(sentence.lchild)
            elif (~sentence.lchild).validate(set(input_list + parsed_list)):
                input_list.append(~sentence.rchild)
            elif (~sentence.rchild).validate(set(input_list + parsed_list)):
                input_list.append(~sentence.lchild)

    return set(parsed_list)