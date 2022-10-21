import pandas as pd
import subprocess
import time

import dash
from dash import html, callback, dcc, dash_table, DiskcacheManager
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output


# Diskcache for non-production apps when developing locally
import diskcache
cache = diskcache.Cache("./cache")
background_callback_manager = DiskcacheManager(cache)

df_input = pd.read_excel(r'C:\Users\anna.muraveva\Documents\SAS\Услуги.xlsx')
# r'C:\Users\anna.muraveva\Documents\SAS\Услуги.xlsx'
# df_output = pd.read_excel(r'C:\Users\anna.muraveva\Documents\SAS\Excel output.xlsx')
# df_output_test = pd.read_csv(r'C:\Users\anna.muraveva\Documents\SAS\rule_engine\matching_rules_stoma.csv')

BTNS_STYLE = {
    'display': 'flex',
    'justify-content': 'right',
    'box-sizing': 'border-box',
}
ASIDE_STYLE = {
    "background-color": "#f8f9fa",
    'white-space': 'pre-line',
    'height': 'calc(100vh - 170px)',
    'overflow': 'scroll',
    # 'position': 'sticky',
    'top': '53px',
}

# Область загрузки файла
download_space = html.Div(
            dcc.Upload(
                id='upload-data_dent',
                children=html.Div([
                    'Перетащите или ',
                    html.A('выберите файл', className="alert-link")
                ]),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px',
                    'color': '#1890ff'
                },
                # Allow multiple files to be uploaded
                multiple=False
            )),

# Область обработки файла
buttons_result = html.Div([
    dbc.Button("Обработать данные", id="btn_prep_xlsx_dent", color="primary", className="me-1", disabled=True,),
    dcc.Download(id="download-dataframe-xlsx_dent"),
    ],
    style=BTNS_STYLE,
)

# Область процесса загрузки
load_progress = dcc.Loading(
            id="loading_dent",
            type="dot",
            children=html.Div(id="loading-output-1"),
            fullscreen=False,
        )
# table_test = html.Div([
#             dash_table.DataTable(
#                 data=df_output_test.to_dict('records'),
#                 columns=[{'name': i, 'id': i} for i in df_output_test.columns],
#                 style_data={
#                             # 'whiteSpace': 'normal',
#                             'height': 'auto',
#                             'lineHeight': '10px',
#                             'minWidth': '180px', 'width': '180px', 'maxWidth': '300px',
#                 },
#
#                 tooltip_data=[
#                     {
#                         column: {'value': str(value), 'type': 'markdown'}
#                         for column, value in row.items()
#                     } for row in df_output_test.to_dict('records')
#                 ],
#                 tooltip_duration=None,
#
#                 style_cell={'textAlign': 'left',
#                             'textOverflow': 'ellipsis',} # left align text in columns for readability
#                     ),
#         ])
#

# Область отображения итоговой таблицы
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
        ])


# Итоговый layout
layout = dbc.Container([
    dbc.Row([
        dbc.Col(download_space, md=4),
        dbc.Col(html.Div(id='upload_status_dent'), md=3, align="center", style={'font-weight': '500', 'color': '#6c757d'}),
        dbc.Col(buttons_result, md=3, align="center"),
        dbc.Col(load_progress, md=2, align="center", style={'justify-content': 'left'}),
    ],
    justify="between"),
    html.Div(id='print_id'),
    html.Div(id='output-table_dent', style=ASIDE_STYLE),
])

# Разблокировка кнопки "Обработать данные" при загрузке данных
@callback(
    Output("upload_status_dent", "children"),
    Output("btn_prep_xlsx_dent", "disabled"),
    Input('upload-data_dent', 'filename'),
    prevent_initial_call=True,)
def show_upload_status_dent(filename):
     return 'Загружен файл {}'.format(filename), False
#
# # Действия при нажатии на кнопку "Обработать файл"
# @callback(
#     Output("output-table_dent", "children"),
#     Output("download-dataframe-xlsx_dent", "data"),
#     Output("loading_dent", "children"),
#     Input("btn_prep_xlsx_dent", "n_clicks"),
#     # prevent_initial_call=True,
#     background=True,
#     manager=background_callback_manager,
#     running=[
#         (Output("btn_prep_xlsx_dent", "disabled"), True, False),
#     ],
#     prevent_initial_call=True
# )
# def show_result_table_dent(n_clicks):
#     time.sleep(2.0)
#     table_test = creat_table(df_output_test)
#     if n_clicks is None:
#         raise dash.exceptions.PreventUpdate
#     else:
#         return table_test, dcc.send_data_frame(df_output_test.to_excel, "df_output.xlsx", sheet_name="Sheet_name_1"), " "


# # Разблокировка кнопки "Обработать данные" при загрузке данных
# @callback(
#     Output("upload_status_dent", "children"),
#     Output("btn_prep_xlsx_dent", "disabled"),
#     Output("output-table_dent", "children"),
#     Input('upload-data_dent', 'contents'),
#     Input('upload-data_dent', 'filename'))
# # prevent_initial_call=True,)
# def show_upload_status_dent(contents, filename):
#     table = creat_table(contents)
#     return 'Загружен файл {}'.format(filename), False, table


# Действия при нажатии на кнопку "Обработать файл"
@callback(
    Output("output-table_dent", "children"),
    Output("download-dataframe-xlsx_dent", "data"),
    Output("loading_dent", "children"),
    # Output("print_id", "children"),
    Input("btn_prep_xlsx_dent", "n_clicks"),
    # prevent_initial_call=True,
    background=True,
    manager=background_callback_manager,
    running=[
        (Output("btn_prep_xlsx_dent", "disabled"), True, False),
    ],
    prevent_initial_call=True
)
def show_result_table_dent(n_clicks):
    # ЗАПУСК ДВИЖКА
    subprocess.run(["python", "main.py", r'C:\Users\anna.muraveva\Documents\SAS\Услуги.xlsx', 'rules_stoma', '-p', 'basic', '-o', 'matching_rules_stoma.csv'],
                            capture_output=False,
                            cwd=r'C:\Users\anna.muraveva\Documents\SAS\rule_engine')

    table_path = r'C:\Users\anna.muraveva\Documents\SAS\rule_engine\matching_rules_stoma.csv'
    table = pd.read_csv(table_path)
    # time.sleep(2.0)

    if n_clicks is None:
        raise dash.exceptions.PreventUpdate
    else:
        return creat_table(table), dcc.send_data_frame(table.to_excel, "РААААБОТАЕТ.xlsx", sheet_name="Sheet_name_1"), " "

