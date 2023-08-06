# TODO: Explicitly import each decorator in release


from typing import List

from pandas import DataFrame

from europy.decorator import test, bias, data_bias, fairness, transparency, accountability, unit, integration, \
    minimum_functionality, model_details, using_params
from europy.decorator.factories import decorator_factory
from europy.lifecycle.model_details import ModelDetails
from europy.lifecycle.reporting import execute_tests, report_model_details, report_model_params, generate_report
from europy.lifecycle.result import TestLabel, TestResult

# This is how you make your own decorator for tests with a custom label or with a provided label

EXAMPLE_LABEL_NAME = "my-custom-label"


def custom_decorator(name: str = ""):
    labels = ["my-custom-decorator-label", TestLabel.MINIMUM_FUNCTIONALITY]
    return decorator_factory(labels, name)


df = DataFrame([[1, 2], [3, 4]], columns=['odds', 'evens'])


def sample_plot(title: str):
    import matplotlib.pyplot as plt
    import numpy as np

    plt.style.use('fivethirtyeight')

    x = np.linspace(0, 10)

    # Fixing random state for reproducibility
    np.random.seed(19680801)

    fig, ax = plt.subplots()

    ax.plot(x, np.sin(x) + x + np.random.randn(50))
    ax.plot(x, np.sin(x) + 0.5 * x + np.random.randn(50))
    ax.plot(x, np.sin(x) + 2 * x + np.random.randn(50))
    ax.plot(x, np.sin(x) - 0.5 * x + np.random.randn(50))
    ax.plot(x, np.sin(x) - 2 * x + np.random.randn(50))
    ax.plot(x, np.sin(x) + np.random.randn(50))
    ax.set_title(title)

    return plt


# This is how you can create your own labels on the fly
@test(EXAMPLE_LABEL_NAME, "My custom label test")
def custom_label():
    assert True
    return df


@custom_decorator("Test with custom decorator")
def custom_decorator():
    assert True
    return df


# This is an example on using raw decorator
@bias("Testing it out")
def sample_with_raw_decorator():
    assert True
    return df


@data_bias("example data bias test")
def data_bias():
    assert True
    return df


# This is an example on using raw decorator
@fairness("Example Fairness Test")
def fairness_example():
    assert True
    return "Its Fair!"


@transparency("Example Transparency Test")
def transparency_example(plots: dict):
    assert True
    plots["transparency"] = sample_plot("transparency")
    return "It's easy to understand!"


@accountability("Example Accountability Test")
def accountability_example():
    assert True
    return "expectations are defined!"


# This is an example on using raw decorator
@unit("Example Unit Test")
def unit_example():
    assert True


# This is an example on using raw decorator
@integration("Example Integration Test")
def integration_example():
    assert True


# This is an example on using raw decorator
@minimum_functionality("Example Minimum Functionality Test")
def minimum_functionality_example():
    assert True


# This is an example on using raw decorator
@model_details('tests/model_details_example.yml')
@unit("Example with multiple labels")
@fairness()
@minimum_functionality()
@integration()
@bias()
@test(EXAMPLE_LABEL_NAME)
def multiple_labels():
    return "Woah, what a fair unit test"


@model_details('tests/model_details_example.json')  # this will override the current details in the report
def model_details_json(details: ModelDetails = None):
    import json
    details.description += '... this is a computed description'

    with open('tests/model_details_example.json', 'r') as f:
        loaded_details = ModelDetails(**json.load(f))

        assert loaded_details.title == details.title
        assert loaded_details.description != details.description


@model_details('tests/model_details_example.yml')
def model_details_yaml(details: ModelDetails = None):
    import yaml
    details.description += '... this is computed yaml description'

    with open('tests/model_details_example.yml', 'r') as f:
        loaded_details = ModelDetails(**yaml.load(f, Loader=yaml.FullLoader))

        assert loaded_details.title == details.title
        assert loaded_details.description != details.description


# this must run in order to pass
@model_details()  # this will load the latest in the report
def loaded_model_details(details: ModelDetails = None):
    assert '... this is computed yaml description' in details.description


@using_params('tests/param_example.yml')
def params(op1: int = None, op2: int = None, text_example: str = None, list_example: List[float] = [],
           a_global_param=None):
    assert op1 != None, "op1 should be populated from params"
    assert op2 != None, "op1 should be populated from params"
    assert text_example != None, "text_example should be populated from params"
    assert list_example != [], "list_example should be populated from params"
    assert a_global_param != None, "a_global_param should be populated from params"


def test_execute():
    report_model_params('tests/param_example.yml')
    report_model_details('tests/model_details_example.yml')
    results: List[TestResult] = execute_tests(clear=False)
    
    assert all([x.success for x in results])
    assert len(results) == 11

    generate_report(export_type='markdown', clear_report=False)


def test_execute_clear():
    results: List[TestResult] = execute_tests(clear=True)
    assert len(results) == 11

    @fairness("Example Fairness Test")
    def fairness_example():
        assert True
        return "Its Fair!"

    results: List[TestResult] = execute_tests()
    assert len(results) == 1

    generate_report(export_type='markdown')
