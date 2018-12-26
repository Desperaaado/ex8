# conding:utf-8

import sys
import argparse

def argv():
    parser = argparse.ArgumentParser(
        description='Realize sth like "cut" command.'
    )
    parser.add_argument('-character', help='cut by character.')
    parser.add_argument('-byte', help='cut by byte.')
    parser.add_argument('-field', help='cut by field.')
    parser.add_argument('-divide', help='define the separator.')
    parser.add_argument(
        'content',
        help='the content or the file to be cut.',
        nargs='?'
    )
    return parser.parse_args()

def get_lines(content):

    if content:
        content_n = open(content).readlines()
    else:
        content_n = list(sys.stdin)

    the_content = []

    for line in content_n:
        if line != '\n':
            the_line = line[:-1]
            the_content.append(the_line)

    return the_content

def get_settings(character, byte, field, divide):
    if character:
        if not divide:
            divide = None
        return ('char', character, divide)

    elif byte:
        if not divide:
            divide = None
        return ('byte', byte, divide)

    elif field:
        if not divide:
            divide = '  ' # default: cut by "\t"
        return ('field', field, divide)

    else:
        print('You must choose a mode.(-c, -b, -f)')
        sys.exit(1)

def cut_line_to_pieces(line, divide):
    pieces = line.split(divide)
    if not divide:
        return pieces[0]
    else:
        return pieces

def processing_demand(demand):
    if not ('-' in demand):
        print('ERROR: Wrong Condition!(e.g: 2-7)')
        sys.exit(1)

    demand_list = demand.split('-')
    demand_start = demand_list[0]
    demand_end = demand_list[1]

    if demand_start == '':
        demand_start = None
    elif not demand_start.isdigit():
        print('ERROR: Wrong Condition!(e.g: 2-7)')
        sys.exit(1)
    else:
        demand_start = int(demand_start) - 1

    if demand_end == '':
        demand_end = None
    elif not demand_end.isdigit():
        print('ERROR: Wrong Condition!(e.g: 2-7)')
        sys.exit(1)
    else:
        demand_end = int(demand_end)

    return demand_start, demand_end

def processing_pieces(pieces, demand):
    print('line: ', pieces)
    start_num, end_num = processing_demand(demand)

    processed_pieces = pieces[start_num : end_num]
    print('result: ', end='')

    for stuff in processed_pieces:
        print(stuff, end='')
    print('\n')

def cut_text_lists(text_lists, settings):
    mode, demand, divide = settings

    for line in text_lists:
        pieces = cut_line_to_pieces(line, divide)
        processing_pieces(pieces, demand)


args = argv()
lines = get_lines(args.content)
setting = get_settings(
    args.character,
    args.byte,
    args.field,
    args.divide
)
cut_text_lists(lines, setting)