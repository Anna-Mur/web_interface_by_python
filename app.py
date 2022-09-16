import dash
from dash import Input, Output, dcc, html, callback
import dash_bootstrap_components as dbc
from pages import hosp_rules, hosp_main, dent_rules, dent_main

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

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
#
# navbar = dbc.Navbar(
#     dbc.Container(
#         [
#             html.Div(
#                 [
#                     dbc.Col(
#                         dbc.NavbarBrand(id='NavBar_name', className="ms-2"),
#                         align="center",
#                         className="g-0"),
#                     tabs,
#                 ],
#                 style={'display': 'flex'}
#             ),
#             dbc.Row(
#                 [
#                     dbc.Col(dbc.NavItem(
#                         dbc.NavLink("Обработка данных", href="/stomatology", style={'color': '#d9d9d9'})),
#                     md=5),
#                     dbc.Col(dbc.NavItem(
#                         dbc.NavLink("Правила", href="/stomatology/rules", style={'color': '#d9d9d9'})),
#                     md=5)
#                 ],
#             ),
#         ]
#     ),
#     color="dark",
#     dark=True,
#     style=NAVBAR_STYLE
# )
nav_hosp = [
        dbc.NavLink("Обработка данных", href="/", style={'color': 'black'}),
        dbc.NavLink("Правила", href="/polyclinic/rules", style={'color': 'black'}),
        dbc.NavLink("Выбрать директорию для правил", style={'color': 'black'})
]


nav_dent = [
        dbc.NavLink("Обработка данных", href="/stomatology", style={'color': '#d9d9d9'}),
        dbc.NavLink("Правила", href="/stomatology/rules", style={'color': '#d9d9d9'})
]


# navbar = dbc.Navbar(dbc.Container(
#         [
#             dbc.Row([
#
#                 dbc.Col(tabs),
#                 dbc.Col(dbc.NavbarBrand(id='NavBar_name', className="ms-2"),
#                         align="center",
#                         className="g-0"),
#             ]),
#             dbc.Nav(id='tab-content')
#         ]),
#     color="dark",
#     dark=True,
#     style=NAVBAR_STYLE
# )

card = dbc.Card(
    [
        dbc.CardHeader(
            tabs
        ),
        dbc.CardBody(dbc.Nav(id='tab-content'), style={'padding': '0'}),
    ]
)

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
            return nav_hosp
        elif active_tab == "dent":
            return nav_dent
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


if __name__ == '__main__':
    app.run_server(debug=True)

