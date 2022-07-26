import yaml
import os
import pandas as pd

path = os.path.join('c:\\','users','martinj15','projects','rokdoc_plugin','data','scenarios','scen1.yaml')
os.path.isfile(path)


with open(path, 'r') as f:
    scenario = yaml.safe_load(f)['scenarios']
    scenario = [scenario[s] for s in scenario]

pd.DataFrame(scenario)

scenario

import base64
import datetime
import io

import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html, dash_table
import yaml

import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

upload_style = {'width': '100%','height': '60px','lineHeight': '60px','borderWidth': '1px',
                'borderStyle': 'dashed', 'borderRadius': '5px','textAlign': 'center',
                'margin': '10px'}

app.layout = html.Div([
    dcc.Upload(
        id='upload-data', 
        children=html.Div(['Drag and Drop or ', html.A('Select Files')]),
        style=upload_style,
        multiple=False
    ),
    html.Div(id='output-data-upload'),
])

def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')

    path = io.StringIO(base64.b64decode(content_string).decode('utf-8'))
    print(path)
    df = pd.read_csv(path, sep=',\t', skiprows=5, engine='python')

    return html.Div([
        dash_table.DataTable(
            df.to_dict('records'),
            [{'name': i, 'id': i} for i in df.columns]
        ),
    ])

@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'))
def update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = [parse_contents(c, n) for c, n in zip(list_of_contents, list_of_names)]
        return children


if __name__ == '__main__':
    print('bear')
    app.run_server(debug=True, port=3838, )