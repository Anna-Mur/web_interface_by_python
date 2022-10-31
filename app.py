import dash
from dash import Input, Output, dcc, html, callback, State
import dash_bootstrap_components as dbc
from pages import hosp_rules, hosp_main, dent_rules, dent_main

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions=True

server = app.server

app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

def current_path_rules(med_serv):

    if med_serv == 'hosp':
        p = r'C:\Users\anna.muraveva\Documents\SAS\rule_engine\path_rules_poly.txt'
    else:
        p = r'C:\Users\anna.muraveva\Documents\SAS\rule_engine\path_rules_stoma.txt'

    f_read = open(p, "r", encoding='utf-8')
    last_line = f_read.readlines()[-1]
    return last_line

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
            dbc.Tab(label="Поликлиника", tab_id="hosp", style={'color': 'black'}, active_label_style={"color": "black"}),
            dbc.Tab(label="Стоматология", tab_id="dent", style={'color': '#69727a'}, active_label_style={"color": "black"}),
        ],
        id="tabs",
        active_tab="hosp",
                )

nav_hosp = [
        dbc.NavLink("Обработка данных", href="/"), # style={'color': '#69727a'}),
        dbc.NavLink("Правила", href="/polyclinic/rules"), #, style={'color': '#69727a'}),
        # dbc.Button("Open modal", id="open", n_clicks=0),
        dbc.NavLink("Выбрать директорию для правил", id='path_to_rules_hosp', active='exact'), #, style={'color': '#69727a'})
]

nav_dent = [
        dbc.NavLink("Обработка данных", href="/stomatology", active='exact'), #, style={'color': 'black'}),
        dbc.NavLink("Правила", href="/stomatology/rules", active='exact'), #, style={'color': 'black'}),
        dbc.NavLink("Выбрать директорию для правил", id='path_to_rules_dent'), #, active='exact', style={'color': 'black'})
]


card = dbc.Card(
    [
        dbc.CardHeader(
            tabs
        ),
        dbc.CardBody(dbc.Nav(id='tab-content', style={'pointer-events': 'auto'}), style={'padding': '0'}),
    ]
)
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

modal = dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Выбор директории для правил")),
                dbc.ModalBody([
                    html.Div("Текущая директория"),
                    html.Div(current_path_rules(med_serv='poly')),
                    html.Hr(),
                    # html.Div(),
                    dcc.Upload(html.A('Изменить директорию')),
                    # html.Button('Изменить директорию для правил поликлиники')
                     ]),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close", id="close", className="ms-auto", n_clicks=0
                    )
                ),
            ],
            id="modal",
            is_open=False,
        )

app.layout = html.Div([
    card,
    dcc.Location(id='url', refresh=False),
    modal,
    html.Div(id='page-content', style={'overflow': 'hidden', 'margin-right': 'auto'}),
])

# Выбрать директорию для правил
# @callback(
#     Output("modal", "is_open"),
#     [Input("path_to_rules_hosp", "n_clicks"), Input("close", "n_clicks")],
#     [State("modal", "is_open")]
# )
# def toggle_modal(n1, n2, is_open):
#     if n1 or n2:
#         return not is_open
#     return is_open

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
            # return dbc.Nav(nav_hosp, pills=True, fill=True), url_pathname
        elif active_tab == "dent":
            url_pathname='/stomatology'
            return nav_dent, url_pathname
            # return dbc.Nav(nav_dent, pills=True, fill=True), url_pathname
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
    # app.run_server(debug=True)
    app.run_server(debug=False, dev_tools_ui=False, dev_tools_props_check=False)

