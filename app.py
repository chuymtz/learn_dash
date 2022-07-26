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

app.layout = html.Div([
    data_upload_block,
    # html.Div(id='output-data-upload'),
    html.Div([        html.Div(id='table-placeholder', children=[])    ], className='row'),
    dcc.Store(id='store-data', data=[], storage_type='memory'), # 'local' or 'session'
    
]) 

def make_table(df):
    dff = pd.read_json(df, orient='split')
    return dash_table.DataTable(dff.to_dict('records'), [{'name': i, 'id': i} for i in dff.columns])

def parse_csv_contents(contents, filename):
    content_type, content_string = contents.split(',')
    path = io.StringIO(base64.b64decode(content_string).decode('utf-8'))
    df = pd.read_csv(path, sep=',\t', skiprows=5, engine='python')
    return df


@app.callback(
    Output('store-data', 'data'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'))
def store_data(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = [parse_csv_contents(c, n) for c, n in zip(list_of_contents, list_of_names)]
        # children = children[0].to_dict('records')
        children = children[0].to_json()
        return children
    
@app.callback(
    Output('table-placeholder', 'children'),
    Input('store-data', 'data'),
    prevent_initial_callbacks=True
)
def create_graph1(data):
    if data is not None:
        # dff = pd.DataFrame(data)
        # 2. convert string like JSON to pandas dataframe
        dff = pd.read_json(data)
        my_table = dash_table.DataTable(
            columns=[{"name": i, "id": i} for i in dff.columns],
            data=dff.to_dict('records')
        )
        return my_table


if __name__ == '__main__':
    app.run_server(debug=True, port=3838, )