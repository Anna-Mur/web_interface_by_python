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

btns_dent = html.Div(
    [
        dbc.Row(
            [
                dbc.Button(
                    "Загрузить файл",
                    color="primary",
                    id="button1_dent",
                    className="mb-3",
                ),
                dbc.Button(
                    "Посмотреть правила",
                    color="primary",
                    id="button2_dent",
                    className="mb-3",
                ),

                dbc.Button(
                    "Получить файл",
                    color="primary",
                    id="button3_dent",
                    className="mb-3",
                ),
            ]
        ),
    ],
    id='btns_dent',
    style=BTNS_STYLE
)


layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Tabs(
                    [
                        dbc.Tab(label="Поликлиника", tab_id="hosp"),
                        dbc.Tab(label="Стоматология", tab_id="dent"),
                    ],
                    id="tabs",
                    active_tab="hosp",
                ),
                html.Div(id="tab-content", className="p-4"),
            ]
        ),
    ]
)

layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Tabs(
                    [
                        dbc.Tab(label="Поликлиника", tab_id="hosp"),
                        dbc.Tab(label="Стоматология", tab_id="dent"),
                    ],
                    id="tabs",
                    active_tab="hosp",
                ),
                html.Div(id="tab-content", className="p-4"),
            ]
        ),
    ]
)

# @callback(
#     Output("tab-content", "children"),
#     Input("tabs", "active_tab"),
# )
# def render_tab_content(active_tab):
#     """
#     This callback takes the 'active_tab' property as input, as well as the
#     stored graphs, and renders the tab content depending on what the value of
#     'active_tab' is.
#     """
#     if active_tab is not None:
#         if active_tab == "hosp":
#             return btns_hosp
#         elif active_tab == "dent":
#             return btns_dent
#     return "No tab selected"

# @callback(
#     Output("page-content", "children"),
#     Input("button2", "n_clicks"),
# )
# def open_rules(n_clicks):
#     return rules_page.layout