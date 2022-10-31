import os

import dash
from dash import html, callback, Input, Output, dcc
import dash_treeview_antd
import dash_bootstrap_components as dbc
from funcs import get_tree_data


# dash.register_page(__name__, path='/polyclinic/rules')

path_dir_hosp = 'C:\\Users\\anna.muraveva\\Documents\\SAS\\Rules\\rules_poly'
data_tree_hosp = get_tree_data(path_dir_hosp)


TREE_STYLE = {
    'white-space': 'pre-line'
}

CONTENT_STYLE = {
    'padding-left': '5%',
    'padding-top': '5%',
    'overflow': 'scroll',
    'height': 'calc(100vh - 100px)',
    'top': '53px'
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
        id='input',
        multiple=False,
        checkable=False,
        checked=[],
        selected=[],
        expanded=[],
        data=(data_tree_hosp)),
    style=TREE_STYLE
)
content = html.Div(id="output-selected", style={'white-space': 'pre-wrap'})


layout = dbc.Row(
            [
                dbc.Col(tree, md=4, style=ASIDE_STYLE),
                dbc.Col(content, md=8, style=CONTENT_STYLE)
            ],
        )


@callback(Output('output-selected', 'children'),
              [Input('input', 'selected')])
def on_clicked_hosp(selected_item):
    if isinstance(selected_item, list):
        p = selected_item[0]
        if os.path.isdir(p):
            pass
        else:
            with open(p, 'r', encoding='utf-8') as file:
                return file.read()
