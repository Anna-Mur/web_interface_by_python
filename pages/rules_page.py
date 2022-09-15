import os

from dash import html, callback, Input, Output, dcc
import dash_treeview_antd
import dash_bootstrap_components as dbc
# from dash.dependencies import Input, Output


# dash.register_page(__name__, path='/rules')

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

path_dir = 'C:\\Users\\anna.muraveva\\Documents\\SAS\\Rules\\rules_poly'
tree_dirs = get_tree_data(path_dir)


TREE_STYLE = {
    'white-space': 'pre-line'
}

CONTENT_STYLE = {
    'padding-left': '5%',
    'padding-top': '5%'
}

ASIDE_STYLE = {
    "background-color": "#f8f9fa",
    'white-space': 'pre-line',
    'height': 'calc(100vh - 53px)',
    'overflow': 'scroll',
    # 'position': 'sticky',
    'top': '53px',
}

tree = html.Div(
    dash_treeview_antd.TreeView(
        id='input',
        multiple=False,
        checkable=False,
        checked=[],
        selected=[],
        expanded=[],
        data=(tree_dirs)),
    style=TREE_STYLE
)
content = html.Div(id="output-selected")


# layout = html.Div(
#     [
#         dbc.Row(
#             [
#                 dbc.Col(tree, md=4, style=ASIDE_STYLE),
#                 dbc.Col(content, md=7, style=CONTENT_STYLE)
#             ],
#         ),
#
#     ],
# )
layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(tree, md=4, style=ASIDE_STYLE),
                dbc.Col(content, md=7, style=CONTENT_STYLE)
            ],
        ),

    ],
)

@callback(Output('output-selected', 'children'),
              [Input('input', 'selected')])
def on_clicked(selected):
    if isinstance(selected, list):
        p = selected[0]
        if os.path.isdir(p):
            pass
        else:
            with open(p, 'r', encoding='utf-8') as file:
                return file.read()
