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

data_upload_block = dcc.Upload(id='upload-data',
                               children=html.Div(['Drag and Drop or ', html.A('Select Files') ]), 
                               style=upload_style, 
                               multiple=True )
scenario_upload_block = dcc.Upload(id='upload-scenario',
                               children=html.Div(['Choose scenario file' ]), 
                               style=upload_style, 
                               multiple=True )

app.layout = html.Div([
    data_upload_block,
    scenario_upload_block,
    html.Div(id='output-data-upload'),
    html.Div(id='output-scenario-upload')
])

def make_table(df):
    return html.Div([
        dash_table.DataTable(
            df.to_dict('records'),
            [{'name': i, 'id': i} for i in df.columns]
        ),
    ])

def parse_csv_contents(contents, filename):
    content_type, content_string = contents.split(',')
    path = io.StringIO(base64.b64decode(content_string).decode('utf-8'))
    print(path)
    df = pd.read_csv(path, sep=',\t', skiprows=5, engine='python')
    return df

def parse_scenerio_contents(contents, filename):
    content_type, content_string = contents.split(',')
    path = io.StringIO(base64.b64decode(content_string).decode('utf-8'))
    scenario = yaml.safe_load(path)['scenarios']
    return pd.DataFrame([scenario[s] for s in scenario])

@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'))
def update_table(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = [make_table(parse_csv_contents(c, n)) for c, n in zip(list_of_contents, list_of_names)]
        return children

@app.callback(Output('output-scenario-upload', 'children'),
              Input('upload-scenario', 'contents'),
              State('upload-scenario', 'filename'))
def update_scentable(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = [make_table(parse_scenerio_contents(c, n)) for c, n in zip(list_of_contents, list_of_names)]
        return children

if __name__ == '__main__':
    app.run_server(debug=True, port=3838, )