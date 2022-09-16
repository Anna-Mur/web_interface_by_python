import base64
import datetime
import io
import pandas as pd


import dash
from dash import html, callback, Input, Output, dcc, dash_table, State
import dash_bootstrap_components as dbc


# dash.register_page(__name__, path='/')

BTNS_STYLE = {
    'display': 'flex',
    'justify-content': 'center',
    'box-sizing': 'border-box'
}
ASIDE_STYLE = {
    "background-color": "#f8f9fa",
    'white-space': 'pre-line',
    'height': '60%',
    'overflow': 'scroll',
    # 'position': 'sticky',
    'top': '53px',
}
# btns_hosp = html.Div(
#     [
#         dbc.Row(
#             [
#                 dbc.Button(
#                     "Загрузить файл",
#                     color="primary",
#                     id="button1",
#                     className="mb-3",
#                 ),
#                 dcc.Link(
#                         "Посмотреть правила",
#                         id="button2",
#                         className="mb-3 btn btn-primary",
#                         href='/rules', refresh=False
#                 ),
#
#                 dbc.Button(
#                     "Получить файл",
#                     color="primary",
#                     id="button3",
#                     className="mb-3",
#                 ),
#             ]
#         ),
#     ],
#     id='btns_hosp',
#     style=BTNS_STYLE
# )



download_btn = html.Div(
    [html.Button("Download Xlsx", id="btn_xlsx"), dcc.Download(id="download-xlsx-index")]
)

buttons = html.Div(
    [
        dbc.Button("Обработать данные", color="primary", className="me-1"),
        dbc.Button("Отобразить на экране", color="primary", disabled=True, className="me-1"),
        dbc.Button("Выгрузить файл", color="primary", disabled=True),
    ],
    style=BTNS_STYLE
)

layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                ]),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                },
                # Allow multiple files to be uploaded
                multiple=True
            )
        ),
        dbc.Col(
            buttons, md=5
        )
    ])
    ,
    html.Div(id='output-data-upload', style=ASIDE_STYLE),
])

# layout = dbc.Container(
#     [
#
#         dbc.Row(
#             upload_space
#         ),
#         dbc.Row(
#             download_btn
#         ),
#     ]
# )

# layout = html.Div(
#     [
#         dbc.Row(
#             upload_space
#         ),
#         dbc.Row(
#             download_btn
#          ),
#     ],
# )

@callback(Output("download-xlsx-index", "data"), Input("btn_xlsx", "n_clicks"))
def func(n_clicks):
    if n_clicks is None:
        raise dash.exceptions.PreventUpdate
    else:
        return dict(content="Hello world!", filename="hello.txt")

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            df.to_dict('records'),
            [{'name': i, 'id': i} for i in df.columns]
        ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])

@callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

# layout = html.Div(btns_hosp)

# layout = dbc.Container(
#     [
#         dbc.Row(
#             [
#                 dbc.Tabs(
#                     [
#                         dbc.Tab(label="Поликлиника", tab_id="hosp"),
#                         dbc.Tab(label="Стоматология", tab_id="dent"),
#                     ],
#                     id="tabs",
#                     active_tab="hosp",
#                 ),
#                 html.Div(id="tab-content", className="p-4"),
#             ]
#         ),
#     ]
# )


# @callback(
#     Output("page-content", "children"),
#     Input("button2", "n_clicks"),
# )
# def open_rules(n_clicks):
#     return rules_page.layout