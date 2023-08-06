import re

if __name__ == '__main__':
    pass


def f_index(s):
    if s == '' or s == '+':
        return 1.0
    if s == '-':
        return -1.0
    return float(s)


def fix_zero(A):
    '''
    将A中各个数组元素用0补齐，保证各个数组长度一样
    '''
    len_list = [len(item) for item in A]
    max_len = max(len_list)
    for item in A:
        if len(item) < max_len:
            item.extend([0] * (max_len - len(item)))
    return A


def parse_line(s1, ch='x', equal_char=True):
    '''
    解析一行 输入示例 x1+6x2-2x3+x6 = 9
    :param s1: 输入的字符串
    :param ch: 变量表示的字符 默认为x
    :param equal_char: 是否有等式 默认为有
    :return: 返回解析之后的系数
    '''
    s1 = s1.replace(' ', '')
    item_list = []
    if equal_char:
        slist = s1.split('=')
        s1 = slist[0]
        # 如果没有设定equal_char=False 但是表达式中没有= 则程序设定equal_char=False
        if len(slist) == 1:
            equal_char = False
    r_pattern = r'(.*?{}[0-9]+)'.format(ch)
    res = re.findall(r_pattern, s1)
    for item in res:
        i = item.split(ch)
        item_list.append((int(i[1]), f_index(i[0])))
    max_index = sorted(item_list, reverse=True)[0][0]
    ch_list = [0] * max_index
    for item in item_list:
        ch_list[item[0] - 1] = item[1]
    ans = {'A': ch_list, 'B': None}
    if equal_char:
        ans['B'] = int(slist[1])
    return ans


def parse_lines(lines, ch='x'):
    A = []
    B = []
    lines_list = lines.split('\n')
    for item in lines_list:
        ans = parse_line(item, ch=ch)
        A.append(ans['A'])
        B.append(ans['B'])
    return_ans = {'A': fix_zero(A), 'B': B}
    return return_ans


def do_parse_line(s1, ch='x', equal_char=True):
    if s1 == '':
        return ''
    ans = parse_line(s1, ch=ch, equal_char=equal_char)
    temp_list = ans['A']
    temp = [str(i) for i in temp_list]
    temp_s = ' '.join(temp)
    # ans['A'] = str(ans['A'])
    # ans['B'] = str(ans['B'])
    return temp_s


def do_parse_lines(s1, ch='x'):
    if s1 == '':
        return ''
    temp_ans = parse_lines(lines=s1, ch=ch)
    A = temp_ans['A']
    str_A = []
    for item in A:
        str_A.append(' '.join([str(i) for i in item]))
    re_str = '\n'.join(str_A)
    return re_str

def varify():
    ss = '''-9x1 + 6x2 - 23 x3 - 222x6=3
    3x1 + 0.5x2 -x4 -9x7=9'''
    print(do_parse_lines(ss))
