from dash import dcc
from dash import html
from dash.dash import base64
import dash_bootstrap_components as dbc
from dash import dash_table
import pandas as pd
import dash
import base64
import datetime
import io
from dash.dependencies import Output, Input, State
import plotly.express as px
 
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
           suppress_callback_exceptions=True)

app.layout = dbc.Container(
    [
        dcc.Upload(id = 'upload-data',
                   children=html.Div(['Drag and Drop or',html.A('Select')]),
                   style={'width':'100%', 'height':'60px','lineHeight':'60px',
                          'borderWidth':'1px','borderStyle':'dashed',
                          'borderRadius':'5px','textAlign':'center',
                          'margin':'10px'},
                   multiple=True),
        html.Div(id='output-div'),
        html.Div(id='output-datatable')
    ]
)

def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')

    path = io.StringIO(base64.b64decode(content_string).decode('utf-8'))
    print(path)
    df = pd.read_csv(path)

    return html.Div([
        html.H5(filename),
        html.P("Inset X axis data"),
        dcc.Dropdown(id='xaxis-data', options=[{'label':x, 'value':x} for x in df.columns]),
        html.P("Inset Y axis data"),
        dcc.Dropdown(id='yaxis-data',
                     options=[{'label':x, 'value':x} for x in df.columns]),
        html.Button(id="submit-button", children="Create Graph"),
        html.Hr(),

        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns],
            page_size=15
        ),
        dcc.Store(id='stored-data', data=df.to_dict('records')),
        html.Hr(),  # horizontal line
      
        html.Br()
    ])

@app.callback(Output('output-datatable', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'))
def update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = [parse_contents(c, n) for c, n in zip(list_of_contents, list_of_names)]
        return children


@app.callback(Output('output-div', 'children'),
              Input('submit-button','n_clicks'),
              Input('stored-data','data'),
              State('xaxis-data','value'),
              State('yaxis-data', 'value'))
def make_graphs(n, data, x_data, y_data):
    if x_data is None:
        return dash.no_update
    else:
        bar_fig = px.bar(data, x=x_data, y=y_data)
        # print(data)
        return dcc.Graph(figure=bar_fig)
if __name__ == '__main__':
    print('bear')
    app.run_server(debug=True, port=8888, )