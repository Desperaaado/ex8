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
    parser.add_argument('content',help='the content or the file to be cut.')
    return parser.parse_args()

def get_lines(content):
    if content:
        content_n = open(content).readlines()
        the_content = []

        for line in content_n:
            if line != '\n':
                the_line = line[:-1]
                the_content.append(the_line)
        return the_content
    else:
        the_content = sys.stdin
        print(the_content, '\n', '*'*10) ##########
        print('*'*20, list(the_content))
        return list(the_content)

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

def fix_end_num(array, end_num):
    # end_num 需要一些额外的处理以应对 index < 0 的情况
    # 以及之后切片时可能出现的 差一错误
    array_len = len(array)
    num_abs = abs(end_num)
    f_end = end_num

    # index > 0
    if end_num > 0:
        if num_abs > (array_len - 1):
            f_end = array_len
        else:
            f_end = end_num + 1 # +1 是切片需要
    # index < 0
    elif end_num < 0:
        if num_abs > (array_len + 1):
            f_end = (array_len + 1) * (-1) # +1 是切片需要
        elif end_num == -1:
            return None
    # index == 0
    elif end_num == 0 :
        f_end = 1
    else:
        print('ERROR: Wrong Condition!(e.g: 2-7)')
        sys.exit(1)
    
    return f_end

def try_array(array, num):
    try:
        array[num]
        return True
    except IndexError:
        return False

def processing_demand(demand):
    if not ('-' in demand):
        print('ERROR: Wrong Condition!(e.g: 2-7)')
        sys.exit(1)

    demand_list = demand.split('-')
    demand_start = demand_list[0]
    demand_end = demand_list[1]

    if demand_start == '':
        demand_start = str(0 + 1)
    if demand_end == '':
        demand_end = str(-1 + 1)

    if not (demand_start.isdigit() or demand_end.isdigit()):
        print('ERROR: Wrong Condition!(e.g: 2-7)')
        sys.exit(1)
    else:
        start_num = int(demand_start) - 1 # index 从 0 计数，故 -1
        end_num = int(demand_end) - 1 # index 从 0 计数，故 -1

    return start_num, end_num

def processing_pieces(pieces, demand):

    print('>'*5, 'pieces: ', pieces)
    start_num, end_num = processing_demand(demand)
    f_end_num = fix_end_num(pieces, end_num)

    if start_num < 0 or start_num > len(pieces) - 1:
        start_num = 0

    processed_pieces = pieces[start_num : f_end_num]
    
    for stuff in processed_pieces:
        print(stuff, end='')
    print('\n')

def cut_text_lists(text_lists, settings):
    mode, demand, divide = settings
    print('>>mode: ', mode)

    for line in text_lists:
        if line == '\n':
            continue
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