#!/usr/bin/env python3
# --coding: utf-8 --

import argparse
from random import randint


MAX_NUMBER_OF_NUMBERS = 5  # 构成算式的数字的最大数量
MAX_NUMBER_LIMIT = 100000  # 构成算式中的数字的最大值上限
MIN_NUMBER_LIMIT = -100000  # 构成算式中的数字的最小值下限
MAX_QUANTITY = 200  # 生成题目的最大数量


def gen_operation_symbol():
    """随机生成运算符号

    随机生成'+'或'-'，用于构建题目中的算式。

    :return: str: 生成的运算符号
    """
    return '+' if (randint(0,11) % 2) == 0 else '-'


def format_a_number(num):
    """格式化数字的显示方式，如果是负数，在数字的两边加上()"""
    return '({})'.format(num) if num < 0 else str(num)


def gen_one_question(min_number, max_number, num_of_numbers):
    """生成一道题目

    :param min_number: int型，算式中允许出现的最小数字
    :param max_number: int型，算式中允许出现的最大数字
    :param num_of_numbers: int型，组成算式的数字数量
    :return: 结果list
    """
    results = []
    for i in range(0, num_of_numbers):
        n = randint(min_number, max_number)
        results.append(format_a_number(n) if i > 0 else str(n))
        if i != (num_of_numbers-1):
            results.append(gen_operation_symbol())
    return results


def gen_one_question_not_negative(min_number, max_number, num_of_numbers):
    """生成一道非负结果的测试题目

    保证算式中的数字和计算结果都不为负数。

    :param min_number: int型，算式中允许出现的最小数字
    :param max_number: int型，算式中允许出现的最大数字
    :param num_of_numbers: int型，组成算式的数字数量
    :return: 结果list
    """
    a_fs = list(gen_one_question(min_number, max_number, num_of_numbers))
    if num_of_numbers == 2:
        if a_fs[1].strip() == '-' and int(a_fs[0].strip('()')) < int(a_fs[2].strip('()')):
            a_fs[0], a_fs[2] = a_fs[2], a_fs[0]
        return a_fs
    gen_times = 1
    while eval(' '.join(a_fs)) < 0:
        a_fs = list(gen_one_question(min_number, max_number, num_of_numbers))
        print('gen times: {}'.format(gen_times))
        gen_times += 1

    return a_fs


def trim_parameters(first_num, second_num, num_of_nums, the_quantity, negative, bottom_limit, top_limit, number_limit):
    """对用来生成算式的参数进行剪裁

    使得各参数合法，并且不会造成过大计算负载。

    :param first_num: int型，算式中允许出现的最小或最大数字
    :param second_num: int型，算式中允许出现的最小或最大数字
    :param num_of_nums: int型，组成算式的数字数量
    :param the_quantity: int型，生成的题目数量，最小值为1，最大值为常量MAX_QUANTITY所规定数值
    :param negative: 是否允许出现负数的标志
    :param bottom_limit: int型，算式中允许出现的最小数字的下限，最小不能小于常量MIN_NUMBER_LIMIT所规定数值
    :param top_limit: int型，算式中允许出现的最大数字的上限，最大不能大于常量MAX_NUMBER_LIMIT所规定数值
    :param number_limit: int型，组成算式的数字数量上限，最大不能大于常量MAX_NUMBER_OF_NUMBERS所规定数值
    :return: tuple，经过剪裁后合法的参数：最小数字，最大数字，组成算式的数字数量，题目数量
    """
    min_numb = min(first_num, second_num)
    max_numb = max(first_num, second_num)

    min_numb = max(bottom_limit, min_numb)
    max_numb = min(top_limit, max_numb+1)

    numbers = max(1, num_of_nums)
    numbers = min(number_limit, numbers)

    the_quantity = max(1, the_quantity)

    if not negative:
        min_numb = max(0, min_numb)

    return min_numb, max_numb, numbers, the_quantity


def gen_questions(min_number, max_number, num_of_numbers, the_quantity, negative_flag):
    """生成指定数量的题目

    :param min_number: int型，算式中允许出现的最小数字
    :param max_number: int型，算式中允许出现的最大数字
    :param num_of_numbers: int型，组成算式的数字数量
    :param the_quantity: int型，生成的测试题目数量
    :param negative_flag: 题目中是否允许出现负数的标志
    :return: 生成的题目list
    """
    questions = []
    while len(questions) < the_quantity:
        question_str = ''
        if not negative_flag:
            question_str = ' '.join(gen_one_question_not_negative(min_number, max_number, num_of_numbers))
        else:
            question_str = ' '.join(gen_one_question(min_number, max_number, num_of_numbers))

        if question_str not in questions:
            questions.append(question_str)

    return questions


def gen_question_with_answers(min_number, max_number, num_of_numbers, the_quantity, negative_flag):
    """生成包含答案的指定数量的题目

    :param min_number: int型，算式中允许出现的最小数字
    :param max_number: int型，算式中允许出现的最大数字
    :param num_of_numbers: int型，组成算式的数字数量
    :param the_quantity: int型，生成的测试题目数量
    :param negative_flag: 题目中是否允许出现负数的标志
    :return: 生成包含答案的题目dict，key：题目， value：答案
    """
    results_dict = dict()
    for question in gen_questions(min_number, max_number, num_of_numbers, the_quantity, negative_flag):
        results_dict[question] = eval(question)
    return results_dict


def main(min_number, max_number, num_of_numbers, the_quantity, negative_flag, display_answer):
    if not display_answer:
        questions = gen_questions(min_number, max_number, num_of_numbers, the_quantity, negative_flag)
        print(' = \n'.join(questions) + ' = \n')
    else:
        question_dict = gen_question_with_answers(min_number, max_number, num_of_numbers, the_quantity, negative_flag)
        for key, value in question_dict.items():
            print('{} = {}'.format(key, value))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="生成指定数量的简单加减法数学题")
    parser.add_argument('-q', '--quantity', type=int, default=20, help='生成题目的数量，默认为%(default)s,最多200题')
    parser.add_argument('-m', '--min_number', type=int, default=1, help='题目中出现的最小数字，默认为%(default)s')
    parser.add_argument('-x', '--max_number', type=int, default=50, help='题目中出现的最大数字，默认为%(default)s')
    parser.add_argument('-n', '--number', type=int, default=2, help='算式由多少个数字构成，默认为%(default)s')
    parser.add_argument('-w', '--with_answer', action='count', help='生成显示答案的试题')
    parser.add_argument('-g', '--negative', action='count', help='允许在算式和运算结果中出现负数，不加该选项时为不允许。')

    args = parser.parse_args()

    min_num, max_num, number_of_numbers, quantity = trim_parameters(args.min_number,
                                                                    args.max_number,
                                                                    args.number,
                                                                    args.quantity,
                                                                    args.negative,
                                                                    MIN_NUMBER_LIMIT,
                                                                    MAX_NUMBER_LIMIT,
                                                                    MAX_NUMBER_OF_NUMBERS)

    main(min_num, max_num, number_of_numbers, quantity, args.negative, args.with_answer)