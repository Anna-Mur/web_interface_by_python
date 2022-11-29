import os
import base64
import io
import pandas as pd

from dash import html, dash_table

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



def parse_contents(contents, filename, med_serv):
    content_type, content_string = contents.split(',')

    global df
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)

    if med_serv == 'hosp':
        df.to_excel(r'C:\Users\anna.muraveva\Documents\SAS\rule_engine\Услуги_hosp.xlsx', index=False)
    else:
        df.to_excel(r'C:\Users\anna.muraveva\Documents\SAS\rule_engine\Услуги_dent.xlsx', index=False)


def creat_table(df_output):
    return html.Div([
            dash_table.DataTable(
                data=df_output.to_dict('records'),
                columns=[{'name': i, 'id': i} for i in df_output.columns],
                style_data={
                            # 'whiteSpace': 'normal',
                            'height': 'auto',
                            'lineHeight': '10px',
                            'minWidth': '180px', 'width': '180px', 'maxWidth': '300px',
                },

                tooltip_data=[
                    {
                        column: {'value': str(value), 'type': 'markdown'}
                        for column, value in row.items()
                    } for row in df_output.to_dict('records')
                ],
                tooltip_duration=None,

                style_cell={'textAlign': 'left',
                            'textOverflow': 'ellipsis',} # left align text in columns for readability
                    ),
        ]
    )