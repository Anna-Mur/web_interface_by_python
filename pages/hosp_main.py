import pandas as pd

import dash
from dash import html, callback, Input, Output, dcc, dash_table, State
import dash_bootstrap_components as dbc


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
                id='upload-data',
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


buttons_result = html.Div(
    [
        dbc.Button("Обработать данные", id="btn_prep_xlsx", color="primary", className="me-1", disabled=True,),
        dbc.Button("Отобразить на экране", id="btn_show_xlsx", color="primary", disabled=True, className="me-1"),
        dbc.Button("Выгрузить файл", id="btn_download_xlsx", color="primary", disabled=True, className="me-1"),
        dcc.Download(id="download-dataframe-xlsx"),
    ],
    style=BTNS_STYLE
)

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
        dbc.Col(html.Div(id='upload_status'), align="center", style={'font-weight': '500', 'color':'#6c757d'}),
        dbc.Col(buttons_result, md=5, align="center")

    ]),
    html.Div(id='output-table', style=ASIDE_STYLE),
])



# Разблокировка кнопки "Обработать данные" при загрузке данных
@callback(
    Output("upload_status", "children"),
    Output("btn_prep_xlsx", "disabled"),
    Input('upload-data', 'filename'),
    prevent_initial_call=True,)
def show_upload_status(filename):
     return 'Загружен файл {}'.format(filename), False

# Разблокировка кнопок при нажатии на кнопку "Обработать данные"
@callback(
    Output("btn_show_xlsx", "disabled"),
    Output("btn_download_xlsx", "disabled"),
    Input("btn_prep_xlsx", "n_clicks"),
    prevent_initial_call=True,)
def disabled_btns(n_clicks):
     return False, False

# Скачивание файла с результатами при нажатии кнопки "скачать файл"
@callback(
    Output("download-dataframe-xlsx", "data"),
    Input("btn_download_xlsx", "n_clicks"),
    prevent_initial_call=True,
)
def download_file(n_clicks):
    if n_clicks is None:
        raise dash.exceptions.PreventUpdate
    else:
        return dcc.send_data_frame(df_output.to_excel, "df_output.xlsx", sheet_name="Sheet_name_1")

# Отображение таблицы с результатами при нажатии кнопки "Показать на экране"
@callback(
    Output("output-table", "children"),
    Input("btn_show_xlsx", "n_clicks"),
    prevent_initial_call=True,
)
def show_result_table(n_clicks):
    if n_clicks is None:
        raise dash.exceptions.PreventUpdate
    else:
        return table




# @callback(
#     Output("btn_show_xlsx", "disabled"),
#     Input("btn_prep_xlsx", "n_clicks"),
#     prevent_initial_call=True,)
# def fff(n_clicks):
#      return False
