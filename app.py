import dash
from dash import Input, Output, dcc, html, callback, State
import dash_bootstrap_components as dbc
from pages import hosp_rules, hosp_main, dent_rules, dent_main

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions=True

server = app.server

app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

NAVBAR_STYLE = {
    'position': 'sticky',
    'top': '0',
    'z - index': '1020',
    'display': 'flex',
    'align-items': 'center',
    'padding-top': '0.5rem',
    'padding-bottom': '0.5rem',
    'justify-content': 'left',
}



tabs = dbc.Tabs(
        [
            dbc.Tab(label="Поликлиника", tab_id="hosp", active_label_style={"color": "black", 'font_weight':'bold'}),
            dbc.Tab(label="Стоматология", tab_id="dent", active_label_style={"color": "black"}),
        ],
        id="tabs",
        active_tab="hosp",
                )

nav_hosp = [
        dbc.NavLink("Обработка данных", href="/", active='exact', style={'color': 'black'}),
        dbc.NavLink("Правила", href="/polyclinic/rules", active='exact', style={'color': 'black'}),
        dbc.NavLink("Выбрать директорию для правил", active='exact', style={'color': 'black'})
]

nav_dent = [
        dbc.NavLink("Обработка данных", href="/stomatology", active='exact', style={'color': 'black'}),
        dbc.NavLink("Правила", href="/stomatology/rules", active='exact', style={'color': 'black'}),
        dbc.NavLink("Выбрать директорию для правил", id='path_to_rules', active='exact', style={'color': 'black'})
]


card = dbc.Card(
    [
        dbc.CardHeader(
            tabs
        ),
        dbc.CardBody(dbc.Nav(id='tab-content'), style={'padding': '0'}),
    ]
)

# modal = dbc.Modal(
#             [
#                 dbc.ModalHeader(dbc.ModalTitle("Header")),
#                 dbc.ModalBody("This is the content of the modal"),
#                 dbc.ModalFooter(
#                     dbc.Button(
#                         "Close", id="close", className="ms-auto", n_clicks=0
#                     )
#                 ),
#             ],
#             id="modal",
#             is_open=False,
#         )

app.layout = html.Div([
    card,
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
])

@callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/':
        return hosp_main.layout
    elif pathname == '/polyclinic/rules':
        return hosp_rules.layout
    elif pathname == '/stomatology':
        return dent_main.layout
    elif pathname == '/stomatology/rules':
        return dent_rules.layout
    else:
        return '404'

@callback(
    Output("tab-content", "children"),
    Output('url', 'pathname'),
    Input("tabs", "active_tab"),
)
def render_tab_content(active_tab):
    """
    This callback takes the 'active_tab' property as input, as well as the
    stored graphs, and renders the tab content depending on what the value of
    'active_tab' is.
    """
    if active_tab is not None:
        if active_tab == "hosp":
            url_pathname='/'
            return nav_hosp, url_pathname
        elif active_tab == "dent":
            url_pathname='/stomatology'
            return nav_dent, url_pathname
    return ""

@callback(Output('NavBar_name', 'children'),
              Input('url', 'pathname'))
def navbar_name(pathname):
    if pathname in ['/', '/stomatology']:
        return 'Обработка данных'
    elif pathname in ['/polyclinic/rules', '/stomatology/rules']:
        return 'Просмотр правил'
    else:
        return ''

# Выбрать директорию для правил
# @callback(
#     Output("modal", "is_open"),
#     Input("path_to_rules", "n_clicks"),
#     [State("modal", "is_open")]
# )
# def toggle_modal(n1):
#     # if n1 or n2:
#     #     return not is_open
#     return is_open



if __name__ == '__main__':
    app.run_server(debug=False, dev_tools_ui=False, dev_tools_props_check=False)

