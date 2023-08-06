import json
import os
from typing import Dict
from typing import List

import yaml
from pandas import DataFrame

from europy.lifecycle.model_details import ModelDetails
from europy.lifecycle.report import Report
from europy.lifecycle.result import TestResult
from europy.lifecycle.result_promise import TestPromise
from europy.utils import isnotebook

__tests: dict = dict()
__report = Report()


def put_test(promise: TestPromise):
    key = str(promise.func.__name__)
    if key in __tests.keys():
        current: TestPromise = __tests[key]
        current.merge(promise)
        __tests[key] = current
    else:
        __tests[key] = promise


def clear_tests():
    keys = list(__tests.keys())
    for key in keys:
        del __tests[key]


def capture_model_details(details: ModelDetails):
    __report.model_card.model_details = details


def capture_parameters(name: str, params: Dict):
    # combine parameters
    __report.model_card.parameters[name] = {**__report.model_card.parameters.get(name, {}), **params}


def report_model_params(file_path: str):
    params = {}
    with open(file_path, 'r') as f:
        if os.path.split(file_path)[-1].split('.')[-1] in ['yml', 'yaml']:
            params = yaml.load(f, Loader=yaml.FullLoader)
        else:
            params = json.load(f)

    __report.model_card.parameters = params


def report_model_details(path: str):
    details = ModelDetails.of(path)
    __report.model_card.model_details = details


def execute_tests(clear: bool = True, add_to_report: bool = True, *args, **kwargs):
    global __report

    test_results: List[TestResult] = [__tests[key].execute(__report.directory, *args, **kwargs) for key in
                                      __tests.copy()]
    test_result_df = DataFrame([x.__dict__ for x in test_results])

    if add_to_report:
        for result in test_results:
            __report.capture(result)
            for figure in result.figures:
                __report.figures.append(figure)

    passing_count = len(list(filter(lambda x: x.success, test_results)))
    failing_count = len(list(filter(lambda x: not x.success, test_results)))

    print("========= EuroPy Test Results =========")
    # TODO: Replace this with the markdown file instead of JSON
    print(f"Total Tests: {len(test_results)}")
    print(f"Passing: {passing_count}")
    print(f"Failing: {failing_count}")

    if clear:
        clear_tests()

    return DataFrame(test_result_df) if isnotebook() else test_results


def generate_report(export_type: str = 'markdown', clear_report: bool = True):
    global __report

    if export_type == 'markdown':
        file_name = f'report.md'
        file_path = os.path.join(__report.directory, file_name)
        md = __report.to_markdown()
        md.save(__report.directory, 'report.md')
    elif export_type == 'json':
        file_name = f'report.json'
        file_path = os.path.join(__report.directory, file_name)
        with open(file_path, 'w') as outfile:
            outfile.write(__report.to_dictionaries(pretty=True))

    print("========= EuroPy Report Generated =========")
    print(f"Report output: file://{os.path.join(os.environ['PWD'], __report.directory, file_name)}")

    if clear_report:
        __report = Report()
