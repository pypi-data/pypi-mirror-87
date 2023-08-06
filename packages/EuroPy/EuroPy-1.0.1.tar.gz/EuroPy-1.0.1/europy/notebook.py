import os, json, yaml
import  europy.lifecycle.reporting as reporting
from europy.utils import isnotebook

def load_global_params(path: str, report=True):
    """Load and return global paramss

    Args:
        path (str): path to param file
        report (bool, optional): Add params to EuroPy report. Defaults to True.

    Returns:
        Dict[str:Any]: global params
    """

    params = {}
    with open(path, 'r') as f:
        if os.path.split(path)[-1].split('.')[-1] in ['yml', 'yaml']:
            params = yaml.load(f, Loader=yaml.FullLoader)
        else:
            params = json.load(f)

    global_params = params.get('global', {})

    if report:
        reporting.capture_parameters('global', global_params)
        if isnotebook():
            print(f"========= EuroPy Captured Params: (global) =========")
            for (key, value) in global_params.items():
                print(f'  - global.{key}: {value}')

    return global_params