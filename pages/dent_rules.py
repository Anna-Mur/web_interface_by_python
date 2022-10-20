import os

import dash
from dash import html, callback, Input, Output, dcc
import dash_treeview_antd
import dash_bootstrap_components as dbc
from tree_data_funcs import get_tree_data
# from dash.dependencies import Input, Output


# dash.register_page(__name__, path='/stomatology/rules')

path_dir = 'C:\\Users\\anna.muraveva\\Documents\\SAS\\Rules\\rules_stoma'
data_tree_dent = get_tree_data(path_dir)


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
    'height': 'calc(100vh - 100px)',
    'overflow': 'scroll',
    # 'position': 'sticky',
    'top': '53px',
}

tree = html.Div(
    dash_treeview_antd.TreeView(
        id='input_dent',
        multiple=False,
        checkable=False,
        checked=[],
        selected=[],
        expanded=[],
        data=(data_tree_dent)),
    style=TREE_STYLE
)
content = html.Div(id="output-selected_dent", style={'white-space': 'pre-wrap'})


layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(tree, md=4, style=ASIDE_STYLE),
                dbc.Col(content, md=7, style=CONTENT_STYLE)
            ],
        ),

    ],
)


@callback(Output('output-selected_dent', 'children'),
              [Input('input_dent', 'selected')])
def on_clicked(selected_item):
    if isinstance(selected_item, list):
        p = selected_item[0]
        if os.path.isdir(p):
            pass
        else:
            with open(p, 'r', encoding='utf-8') as file:
                return file.read()
