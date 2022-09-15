import os

import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

path_direct = 'C:\\Users\\anna.muraveva\\Documents\\SAS\\stomatology_rules\\rules_all_levels'

def create_structure_project(path_file):
    accordion_items = []
    n = 660
    for element in os.listdir(path_file):
        element_name = element.replace('_', ' ').partition('.')[0]
        if os.path.isdir(os.path.join(path_file, element)):
            accordion_items.append(
                dbc.AccordionItem(
                    [html.P(dbc.Accordion(
                        create_structure_project(os.path.join(path_file, element))))],
                    title=element_name))
            n += 1
        else:
            accordion_items.append(dbc.AccordionItem([
                dbc.Button("Показать правило", id=element),
            ], title=element_name))
    return accordion_items



accordion_test = html.Div(
    dbc.Accordion(create_structure_project(path_direct), id='accordion')
)

# sidebar = html.Div(
#     [
#         html.H2("Sidebar", className="display-4"),
#         html.Hr(),
#         html.P(
#             "A simple sidebar layout with navigation links", className="lead"
#         ),
#         dbc.Nav(
#             [
#                 dbc.NavLink("Home", href="/", active="exact"),
#                 dbc.NavLink("Page 1", href="/page-1", active="exact"),
#                 dbc.NavLink("Page 2", href="/page-2", active="exact"),
#             ],
#             vertical=True,
#             pills=True,
#         ),
#     ],
#     style=SIDEBAR_STYLE,
# )

content = html.Div(id="page-content", style=CONTENT_STYLE)

# app.layout = html.Div([dcc.Location(id="url"), accordion_test, content])

app.layout = dbc.Container(
    [
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(accordion_test, md=5),
                dbc.Col(dbc.ListGroupItem(id='output_test'))
            ],
            align="center",
        ),
    ],
    fluid=True,
)

@app.callback(Output("output_test", "children"),[Input('accordion', "active_item")])
@app.callback(Output("output_test", "children"),[Input('btn', "btn-primary")])
def change_item(value):
    print(value)
    return f"Item selected: {value}"


# @app.callback(Output("page-content", "children"), [Input("url", "pathname")])
# def render_page_content(pathname):
#     if pathname == "/":
#         with open(path_rule_1, 'r', encoding='utf-8') as file:
#             text_f = file.read()
#         return html.P(text_f)
#     elif pathname == "/page-1":
#         return html.P("This is the content of page 1. Yay!")
#     elif pathname == "/page-2":
#         return html.P("Oh cool, this is page 2!")
#     # If the user tries to reach a different page, return a 404 message
#     return html.Div(
#         [
#             html.H1("404: Not found", className="text-danger"),
#             html.Hr(),
#             html.P(f"The pathname {pathname} was not recognised..."),
#         ],
#         className="p-3 bg-light rounded-3",
#     )

if __name__ == "__main__":
    app.run_server(debug=True)
    # print(create_structure_project(r'C:\Users\anna.muraveva\Documents\SAS\Тест'))