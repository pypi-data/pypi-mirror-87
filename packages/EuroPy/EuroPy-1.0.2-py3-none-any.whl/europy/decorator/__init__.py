import inspect
import os
from functools import wraps
from typing import Union, List

from europy.decorator.factories import decorator_factory
from europy.lifecycle import reporting
from europy.lifecycle.model_details import ModelDetails
from europy.lifecycle.result import TestLabel
from europy.utils import isnotebook


def test(label: str = "",
         name: str = None,
         description: str = None):
    labels: List[Union[str, TestLabel]] = [label]

    return decorator_factory(labels, name, description)


def bias(name: str = None,
         description: str = None,
         x=None):
    labels: List[Union[str, TestLabel]] = [TestLabel.BIAS]
    return decorator_factory(labels, name, description)


def data_bias(name: str = None,
              description: str = None):
    labels: List[Union[str, TestLabel]] = [TestLabel.DATA_BIAS]

    return decorator_factory(labels, name, description)


def fairness(name: str = None,
             description: str = None):
    labels: List[Union[str, TestLabel]] = [TestLabel.FAIRNESS]

    return decorator_factory(labels, name, description)


def transparency(name: str = None,
                 description: str = None):
    labels: List[Union[str, TestLabel]] = [TestLabel.TRANSPARENCY]

    return decorator_factory(labels, name, description)


def accountability(name: str = None,
                   description: str = None):
    labels: List[Union[str, TestLabel]] = [TestLabel.ACCOUNTABILITY]

    return decorator_factory(labels, name, description)


def accuracy(name: str = None,
             description: str = None):
    labels: List[Union[str, TestLabel]] = [TestLabel.ACCURACY]

    return decorator_factory(labels, name, description)


def unit(name: str = None,
         description: str = None):
    labels: List[Union[str, TestLabel]] = [TestLabel.UNIT]

    return decorator_factory(labels, name, description)


def integration(name: str = None,
                description: str = None):
    labels: List[Union[str, TestLabel]] = [TestLabel.INTEGRATION]

    return decorator_factory(labels, name, description)


def minimum_functionality(name: str = None,
                          description: str = None):
    labels: List[Union[str, TestLabel]] = [TestLabel.MINIMUM_FUNCTIONALITY]

    return decorator_factory(labels, name, description)


def model_details(file_path: str = None):
    """Adds a model details to the Report.

    Args:
        file_path (str, optional): Path to model details JSON file. Defaults to None.
    """

    def inner_wrapper(func):

        @wraps(func)
        def inner_func_wrapper(*args, **kwargs):
            import json, yaml

            # pull current report (generated @ __init__)
            details = reporting.__report.model_card.details

            func_spec = inspect.getfullargspec(func)

            # load details into the func arguments (optional)
            if 'details' in func_spec.args:
                kwargs['details'] = details

            result = func(*args, **kwargs)

            # capture model details **after** func is executed
            reporting.capture_model_details(details)

            return result

        return inner_func_wrapper

    return inner_wrapper


def using_params(file_path: str, report=True):
    """allows params for a function to be injected from a yaml or json file

    NOTE: parameters should be prefixed with function name,
    ```yaml
    a_func.param1 = 1.2
    a_different_func.param1 = 1.4
    global_param1 = 1e-6
    ```
    only parameters with a matching prefix will be used. this matches the implementation of gin.config.

    Args:
        file_path (str): relative path to the paramters file (.json, .yaml, or .yml)
        report (bool, optional): should include in model card report. Defaults to True.
    """

    def inner_wrapper(func):
        @wraps(func)
        def inner_func_wrapper(*args, **kwargs):
            import json, yaml

            func_name = func.__name__

            file_name = os.path.split(file_path)[0]
            func_spec = inspect.getfullargspec(func)
            if report:
                params = reporting.__report.model_card.parameters.get(func_name, {})
            else:
                params = {}

            with open(file_path, 'r') as f:
                if os.path.split(file_path)[-1].split('.')[-1] in ['yml', 'yaml']:
                    params = yaml.load(f, Loader=yaml.FullLoader)
                else:
                    params = json.load(f)

            # global params
            global_loaded_params = {}
            for (key, value) in params.get('global', {}).items():
                if key in func_spec.args:
                    global_loaded_params[key] = value
                    kwargs[key] = value

            # func specific params
            func_loaded_params = {}
            for (key, value) in params.get(func_name, {}).items():
                if key in func_spec.args:
                    func_loaded_params[key] = value
                    kwargs[key] = value

            result = func(*args, **kwargs)

            """ may want to name it something other than the function name
                maybe try to pull a key from the doc string first, or
                give a special key in yaml
            """
            if report:
                reporting.capture_parameters(func_name, kwargs)
                if isnotebook():
                    print(f"========= EuroPy Captured Params: ({func_name}) =========")
                    for (key, value) in global_loaded_params.items():
                        print(f'  - global.{key}: {value}')
                    for (key, value) in func_loaded_params.items():
                        print(f'  - {func_name}.{key}: {value}')

            return result

        return inner_func_wrapper

    return inner_wrapper
