import json
from enum import Enum
from types import TracebackType
from typing import Union, List, Tuple, Type

from _pytest.mark import Mark
from pandas import DataFrame

from europy.lifecycle.markdowner import Markdown
from europy.lifecycle.report_figure import ReportFigure


class TestLabel(str, Enum):
    BIAS = "bias"
    DATA_BIAS = "data-bias"
    FAIRNESS = "fairness"
    TRANSPARENCY = "transparency"
    ACCOUNTABILITY = "accountability"
    UNIT = "unit"
    INTEGRATION = "integration"
    ACCURACY = "accuracy"
    MINIMUM_FUNCTIONALITY = "minimum-functionality"

    @staticmethod
    def of(mark: Mark):
        return TestLabel(mark.name)

    def __json__(self):
        return str(self.value)

    def __str__(self):
        return str(self.value)


class TestResult:
    def __init__(self,
                 key: str,
                 labels: List[str]=[],
                 result: Union[
                     float, str, bool, DataFrame, Tuple[Type[BaseException], BaseException, TracebackType], Tuple[
                         None, None, None]]="",
                 figures: [ReportFigure]=[],
                 description: str="",
                 success: bool=False):
        self.key = key
        self.description = description if description is not None else ""
        self.labels = labels
        self.result = result
        self.figures: [ReportFigure] = figures
        self.success = success

    def to_markdown(self, level=3):
        md = Markdown()
        md.add_header(self.key, level)
    
        md.add_text(self.description)
        
        
        label_list = [f'`{l}`' for l in self.labels]
        md.add_md_content(f'**Labels**: {", ".join(label_list)}')

        md.add_md_content(f'**Results**: (Success: {self.success})\n')
        if isinstance(self.result, DataFrame):
            md.add_data_frame(self.result)
        if isinstance(self.result, str):
            md.add_text(self.result)
        if isinstance(self.result, Tuple):
            md.add_text(f'{self.tuple}')             
            # mdTestResult.add_dict_content(
            #     json.loads(json.dumps(self.result.__dict__)))  # couldn't test enough this part

        if len(self.figures) > 0:
            md.add_header('Figures', level+1)
            md.add_image_array(self.figures) 
        return md
