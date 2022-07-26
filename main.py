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

