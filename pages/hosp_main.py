import dash
from dash import html, callback, Input, Output, dcc
import dash_bootstrap_components as dbc


# dash.register_page(__name__, path='/')

BTNS_STYLE = {
    'display': 'flex',
    'justify-content': 'center',
}

btns_hosp = html.Div(
    [
        dbc.Row(
            [
                dbc.Button(
                    "Загрузить файл",
                    color="primary",
                    id="button1",
                    className="mb-3",
                ),
                dcc.Link(
                        "Посмотреть правила",
                        id="button2",
                        className="mb-3 btn btn-primary",
                        href='/rules', refresh=False
                ),

                dbc.Button(
                    "Получить файл",
                    color="primary",
                    id="button3",
                    className="mb-3",
                ),
            ]
        ),
    ],
    id='btns_hosp',
    style=BTNS_STYLE
)

layout = html.Div(btns_hosp)

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