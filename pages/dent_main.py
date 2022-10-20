import pandas as pd
import time

import dash
from dash import html, callback, Input, Output, dcc, dash_table, State, DiskcacheManager
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output


# Diskcache for non-production apps when developing locally
import diskcache
cache = diskcache.Cache("./cache")
background_callback_manager = DiskcacheManager(cache)

df_input = pd.read_excel(r'C:\Users\anna.muraveva\Documents\SAS\Excel input.xlsx')
df_output = pd.read_excel(r'C:\Users\anna.muraveva\Documents\SAS\Excel output.xlsx')



BTNS_STYLE = {
    'display': 'flex',
    'justify-content': 'center',
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

buttons_result = dbc.Container(
    dbc.Row([

        dbc.Col(dbc.Button("Обработать данные", id="btn_prep_xlsx_dent", color="primary", className="me-1", disabled=True,)),
        dbc.Col(dcc.Loading(
            id="ls-loading-1",
            type="dot",
            children=html.Div(id="loading-output-1"),
            fullscreen=False,
        ),
            align="center"),
        dcc.Download(id="download-dataframe-xlsx_dent"),
    ],
    style=BTNS_STYLE
))

table = html.Div([
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

layout = dbc.Container([
    dbc.Row([
        dbc.Col(download_space),
        dbc.Col(html.Div(id='upload_status_dent'), align="center", style={'font-weight': '500', 'color': '#6c757d'}),
        dbc.Col(buttons_result, md=5, align="center")
    ]),
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

# # Разблокировка кнопок при нажатии на кнопку "Обработать данные"
# @callback(
#     Output("btn_prep_xlsx_dent", "disabled"),
#     Input("btn_prep_xlsx_dent", "n_clicks"),
#     prevent_initial_call=True,)
# def disabled_btns_dent(n_clicks):
#      return False

# Скачивание файла с результатами при нажатии кнопки "скачать файл"
# @callback(
#     Output("download-dataframe-xlsx_dent", "data"),
#     Input("btn_prep_xlsx_dent", "n_clicks"),
#     prevent_initial_call=True,
# )
# def download_file_dent(n_clicks):
#     if n_clicks is None:
#         raise dash.exceptions.PreventUpdate
#     else:
#         return dcc.send_data_frame(df_output.to_excel, "df_output.xlsx", sheet_name="Sheet_name_1")

# # Отображение таблицы с результатами при нажатии кнопки "Показать на экране"
# @callback(
#     Output("output-table_dent", "children"),
#     Input("btn_prep_xlsx_dent", "n_clicks"),
#     # prevent_initial_call=True,
#     background=True,
#     manager=background_callback_manager,
# )
# def show_result_table_dent(n_clicks):
#     time.sleep(2.0)
#     if n_clicks is None:
#         raise dash.exceptions.PreventUpdate
#     else:
#         return table


@callback(
    Output("output-table_dent", "children"),
    Output("download-dataframe-xlsx_dent", "data"),
    Output("ls-loading-1", "children"),
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
    time.sleep(2.0)

    if n_clicks is None:
        raise dash.exceptions.PreventUpdate
    else:
        return table, dcc.send_data_frame(df_output.to_excel, "df_output.xlsx", sheet_name="Sheet_name_1"), " "


# @callback(Output("ls-loading-output-1", "children"), Input("btn_prep_xlsx_dent", "n_clicks"))
# def input_triggers_nested(n_clicks):
#     time.sleep(1)
#     return n_clicks