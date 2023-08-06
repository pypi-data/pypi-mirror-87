# EuroPy

EuroPy is a declarative python testing framework designed for the machine learning (ML) pipeline. Inspired by other testing frameworks (such as JUnit and NUnit) EuroPy uses test decorators to register and execute tests.

EuroPy is designed to work within an Iron Python interactive environment (i.e. Jupyter Notebook) as well as within the typical python kernel. 

## Philosophy
As the use of machine learning becomes increasingly common, there is a greater need to address issues of reproducibility and the prevalence of ML systems' unforeseen adverse effects. Doing so requires a more structured approach to evaluating ML systems. EuroPy is a ML testing library that incorporates recommendations from existing literature to aid in the organization and reporting of tests in the ML pipeline. EuroPy is a lightweight testing framework designed to help data scientists and machine learning engineers write and generate results for custom tests to address factors such as Accuracy, Bias, Fairness, Data Bias, Minimum Functionality, etc. that are oftentimes not considered in the development of ML models and pipelines. By encouraging developers to consider potential sources of bias through ML testing, the EuroPy testing framework aims to minimize negative societal impact, address ethical debt, and foster responsible ML prior to deployment. 
## Usage

Creating a test function is accomplished by simply decorating any function with decorators from `europy.decorators`. This will register your test function with the EuroPy lifecycle. In order to execute all registered tests you simply need to execute the `europy.lifecycle.reporting.execute_tests` function. Any parameters passed to the `execute_tests` function will also be passed to all registered functions. 

```python
from europy.decorator import bias, fairness
from europy.lifecycle.reporting import execute_tests, generate_report, report_model_details, report_model_params

@bias("My example bias test", "Lorem ipsum dolor sit amet, consectetur adipiscing elit.")
def foo(input):
    assert input % 2 == 0
    return input

@fairness("My example fairness test that fails")
@bias()
def foo_failure(input): 
    assert input % 2 == 1
    return input

@bias("example_figure")
def save_image_example(plots: dict):
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
    ax.set_title("'fivethirtyeight' style sheet")

    plots['fivethirtyeight_fig'] = plt


report_model_params('tests/param_example.yml')
report_model_details('tests/model_details_example.yml')
execute_tests(clear=True, input=1)
generate_report(export_type='markdown', clear_report=True)
```
Pulled from [this](./testing-notebook.ipynb) notebook

### Example Notebook Output
![Notebook Output](./.img/notebook-output-1.png)

### Example Standard Output
![Standard Output](./.img/standard-output-1.png)

## Testing Report
When the `generate_report` function is called, all recorded tests are flushed to a report file. The report can be exported in markdown or JSON format. An example of a testing report for the above example can be found [HERE](./.img/report.md)

## Model Card
EuroPy can also help with generating high level details of your model for use in the report. This is included with the `@model_details()` decorator which reads data from `.yaml` or `.json` file. An example can be found at `tests/model_details_example.[yml|json]`.  

### Simple Model Card Example
```python
from europy.decorator import model_details
from europy.lifecycle.model_details import ModelDetails

@model_details('model_details.yml') # will load details from file and pass into train
def train(details: ModelDetails=None):
    # train
    details.description = "something computed"

@model_details() # will load existing details from the current report
def test(detail: ModelDetails=None):
    pass
```

### Including Model details in a Test Report
To include the model details in your test report simply add the model details decoratoer to a test inside of your test suite OR use the `report_model_details` function. Examples of both are below

#### Using a Test Decorator
```python
from europy.decorator import model_details
from europy.lifecycle.model_details import  ModelDetails
from europy.lifecycle.reporting import execute_tests, generate_report

@model_details('model-details.yml') 
def loaded_model_details(details: ModelDetails = None):
    # You can also manipulate your details object HERE if you wish
    pass

execute_tests()
generate_report()
```

#### Using the `report_model_details` function
```python
from europy.lifecycle.reporting import execute_tests, generate_report, report_model_details

#... Write Tests

execute_tests()
report_model_details('model-details.yml')
generate_report()
```


## Hyper-Parameters
Keeping track of hyper-parameter tuning can be accomplished in configuration `.yml` or `.json` files and loaded into your code with the decorator `using_params()` or globally with `load_global_params()`. Doing so will automatically add the parameter details to your report. Parameters are loaded from 

### Example Param Usage
```yaml
global:
    num_epochs: 4
    batch_size: 128
    learning_rate: 0.0001
train: 
    test_split: 0.2
test:
    title: "Testing Run 01"
    batch_size: 256
```
```python
from europy.decorator import using_params
@using_params('params.yml')
def train(num_epochs: int=None, batch_size: int=None, learning_rate: float=None, test_split: float=None):
    # will load global params first, then params matching func name
    pass

@using_params('params.yml')
def test(title: str="", batch_size: int=None):
    # will load batch_size from test, overriding the global definition
    pass 
```

### Example Notebook Output
![Global Params Output](./.img/global_params_notebook.png)
![Function Params Capture](./.img/func_params_notebook.png)

### Including Model Parameters in a Test Report
To include the model parameters in your test report simply add the using_params decorator to a test inside of your test suite OR use the `report_model_params` function. Examples of both are below

#### Using a Test Decorator
```python
from europy.decorator import using_params
from europy.lifecycle.reporting import execute_tests, generate_report

@using_params('params.yml')
def test(title: str="", batch_size: int=None):
    # will load batch_size from test, overriding the global definition
    pass 

execute_tests()
generate_report()
```

#### Using the `report_model_params` Function
```python
from europy.lifecycle.reporting import execute_tests, generate_report, report_model_params

#... Write Tests to execute

execute_tests()
report_model_params('model-parameters.yml')
generate_report()
```



## Test Decorators
EuroPy supports a number of test classes out of the box. These test classes have been created by surveying industry practitioners and creating a list of well known testing labels. When defining a testing function you may pass two optional parameters to any decorator: name and description. These parameters are used as metadata and will be included in the resulting test report. The supported labels are listed below. 
    
- `@bias()`
- `@data_bias()`
- `@fairness()`
- `@transparency()`
- `@accountability()`
- `@accuracy()`
- `@unit()`
- `@integration()`
- `@minimum_functionality()`

### Custom Test Decorators
While we believe these decorators should be comprehensive we have provided two ways in which you can add your own custom label to the test reports. For the examples below we will be adding a custom "end-to-end" testing label to our testing function. 

- Using the  generic `@test()` decorator you can provide a custom string label
```python
from europy.decorator import test
from europy.lifecycle.reporting import execute_tests

EXAMPLE_LABEL_NAME = "end-to-end"

@test(EXAMPLE_LABEL_NAME, "My custom label test")
def foo(input):
    assert input % 2 == 0
    return input

execute_tests(100)
```
- Defining your own test decorator using the decorator_factory
```python
from europy.decorator import decorator_factory
from europy.lifecycle.reporting import execute_tests

def end_to_end(name: str = ""):
    # here you can add multiple labels if you wish
    labels = ["end-to-end"]
    return decorator_factory(labels, name)


@end_to_end("Test with custom decorator")
def foo(input):
    assert input % 2 == 0
    return input

execute_tests(100)
```
