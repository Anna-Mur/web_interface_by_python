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
    'justify-content': 'left'
}

nav_hosp = [dbc.NavItem(dbc.NavLink("Обработка данных", href="/")),
            dbc.NavItem(dbc.NavLink("Правила", href="/polyclinic/rules"))]

nav_dent = [dbc.NavItem(dbc.NavLink("Обработка данных", href="/stomatology")),
            dbc.NavItem(dbc.NavLink("Правила", href="/stomatology/rules"))]

tabs = dbc.Tabs(
        [
            dbc.Tab(label="Поликлиника", tab_id="hosp"),
            dbc.Tab(label="Стоматология", tab_id="dent"),
        ],
        id="tabs",
        active_tab="hosp",
                )
navbar = dbc.Navbar(
    dbc.Container(
        [
            tabs,
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    dbc.Col(dbc.NavbarBrand(id='NavBar_name', className="ms-2")),
                    align="center",
                    className="g-0",
                ),
                style={"textDecoration": "none"},
            ),

            html.Div(id='tab-content')
        ]
    ),
    color="dark",
    dark=True,
    style=NAVBAR_STYLE
)

app.layout = html.Div([
    navbar,
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
])
#
# app.layout = html.Div([navbar,
#                        dcc.Location(id='url', refresh=False),
#                        html.Div(hosp_rules.layout)])

@callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    print(pathname)
    if pathname == '/':
        print('работает /')
        return hosp_main.layout
    elif pathname == '/polyclinic/rules':
        return hosp_rules.layout
    elif pathname == '/stomatology':
        return dent_main.layout
    elif pathname == '/stomatology/rules':
        print('работает /stomatology/rules')
        return dent_rules.layout
    else:
        return '404'



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
#             return nav_hosp
#         elif active_tab == "dent":
#             return nav_dent
#     return "No tab selected"

# @callback(Output('NavBar_name', 'children'),
#               Input('url', 'pathname'))
# def navbar_name(pathname):
#     if pathname == '/':
#         return 'Главное меню'
#     elif pathname == '/rules':
#         return 'Правила'
#     else:
#         return ''


if __name__ == '__main__':
    app.run_server(debug=True)

