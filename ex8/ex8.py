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

def slice_add_one(end_num):
    # end_num 需要在切片时完成 +1 操作
    # 特别地：当 end_num == -1 时，不作 +1 ，而是直接输出 None
    if end_num == -1 or end_num == None:
        return None
    else:
        return end_num + 1

def num_guarantee(array, num):
    # 保证 num 在 array 的index范围内
    array_len = len(array)
    if num + 1 > array_len:
        return 'too big'   
    elif num < -array_len: 
        return 'too small'
    else:
        return num

def start_end_num_in_range(array, start_num, end_num):
    g_start = num_guarantee(array, start_num)
    g_end = num_guarantee(array, end_num)

    if g_start == 'too big':
        r_start = start_num # 将输出空
    elif g_start == 'too small':
        r_start = None # 将从第一个开始输出
    else:
        r_start = start_num # 正常输出

    if g_end == 'too big':
        r_end = None # 将从最后一个开始输出
    elif g_end == 'too small':
        r_end = end_num # 将输出空
    else:
        r_end = end_num # 正常输出

    # if r_start and r_end and (r_start > r_end): ####
    #     print('ERROR: start_num > end_num')
    #     sys.exit(1)

    return r_start, r_end

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
    r_start, r_end =  start_end_num_in_range(pieces, start_num, end_num)
    processed_pieces = pieces[r_start : slice_add_one(r_end)]
    
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