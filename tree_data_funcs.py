import os

def get_subdict(lst_of_dict: list, title):
    for dct in lst_of_dict:
        if dct['title'] == title:
            return dct

def get_tree_data(path):
    tree = os.walk(path)
    d_q = []
    for element in tree:
        d_q.append(element)

    l = []
    for a, b, c in d_q:
        di = {'title': a.split('\\')[-1], 'key': a}

        if c:
            c = [{'title': c_file.replace('_', ' ').partition('.')[0], 'key': os.path.join(a, c_file)} for c_file in c]
        things = [b, c]
        if any(thing for thing in things):
            di['children'] = things

        l.append(di)

    dirs = []
    for i in l:
        if (i.get('children')):
            if i.get('children')[0]:
                dirs.append(i)
            else:
                i['children'] = i.get('children')[1]
    dirs.reverse()

    for _dirs in dirs:
        child_list = [get_subdict(l, d) for d in _dirs.get('children')[0]]
        if _dirs['children'][1]:
            for i in _dirs['children'][1]:
                child_list.append(i)
        _dirs['children'] = child_list

    tree_dirs = dirs[-1]
    return tree_dirs
