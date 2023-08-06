import errno
import os
from typing import Any, List

from pandas import DataFrame

from europy.lifecycle.report_figure import ReportFigure


class Markdown:
    cls_dict_markdown = ""
    tab = "  "
    list_tag = '* '
    htag = '#'

    def __init__(self):
        self.content = ""

    def save(self, report_directory: str, file_name: str):
        file_path = os.path.join(report_directory, file_name)
        if not os.path.exists(file_path):
            try:
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise
        file = open(file_path, "w")
        file.write(self.content)
        file.close()

    def add_linebreak(self):
        self.content += self.create_block("", 1)
        return self

    def add_list_item(self, text: str, depth: int = 0):
        intent = ""
        if depth > 0:
            intent = "".join([" " * 2] * depth)

        self.content += self.create_block(intent + "- {}".format(text))
        return self

    def add_header(self, text: str, htype: int = 1):
        string = "".join(["#"] * htype) + " {t}".format(t=text)
        self.content += self.create_block(string, 2)
        return self

    def add_text(self, text: str):
        self.content += self.create_block(text, 2)
        return self

    def add_horizontal_line(self):
        self.content += self.create_block("___")
        return self

    def add_block_content(self, *lines: Any):
        _lines: List[str] = list(lines)
        self.content += self.create_block("> " + "  \n".join(_lines), 2)
        return self

    def add_image(self, file_path: str, alt_text: str):
        self.content += self.create_block("![{}]({})".format(alt_text, file_path), 2)
        return self

    def add_image_temp(self, file_path: str, alt_text: str):
        file_path = os.path.join(os.environ['PWD'], file_path)
        self.content += self.create_block("![{}]({})".format(alt_text, file_path), 2)
        return self

    @classmethod
    def create_block(cls, text: str = '', lbcount: int = 1):
        return text + "".join(['\n'] * lbcount)

    def add_table(self, *rows: Any):
        contents: List[List[str]] = list(rows)
        for i, items in enumerate(contents):
            self.content += "| " + "| ".join(items) + "\n"
            if i == 0:
                for item in items:
                    self.content += "| "
                    self.content += "".join(["-"] * len(item))
                self.content += "\n"
        self.content += "\n"
        return self

    def add_data_frame(self, df: DataFrame):
        self.content += self.create_block("", 1)
        self.content += df.to_markdown()
        return self

    def add_image_array(self, figure_arr: [ReportFigure]):
        for fig in figure_arr:
            if not isinstance(fig, ReportFigure):
                self.content += "\n"
                return self
            self.content += "\n"
            self.add_md_content(f"**{fig.title}**")
            self.add_md_content(fig.description)
            self.add_image(fig.img_path, fig.title)
        self.content += "\n"
        return self

    def add_dict_content(self, data, depth):
        self.reset_dict_markdown_data()
        self.content += "\n"
        self.parse_input_data(data, depth)
        self.content += self.getDictMarkdownData()
        self.content += "\n"
        return self

    def add_md_content(self, markdown):
        self.content += "\n"
        self.content += markdown
        self.content += "\n"
        return self

    def __add__(self, other):
        self.content += self.create_block(other.content)
        return self

    @classmethod
    def getDictMarkdownData(cls):
        return cls.cls_dict_markdown

    @classmethod
    def reset_dict_markdown_data(cls):
        cls.cls_dict_markdown = ""

    @classmethod
    def parse_input_data(cls, data, depth):
        if isinstance(data, dict):
            cls.parse_dict(data, depth)
        if isinstance(data, list):
            cls.parse_list(data, depth)

    @classmethod
    def parse_dict(cls, d, depth):
        for k in d:
            if isinstance(d[k], (dict, list)):
                cls._add_header(k, depth)
                cls.parse_input_data(d[k], depth + 1)
            else:
                cls._add_value(k, d[k], depth)

    @classmethod
    def parse_list(cls, lis, depth):
        for value in lis:
            if not isinstance(value, (dict, list)):
                index = lis.index(value)
                cls._add_value(index, value, depth)
            else:
                cls.parse_dict(value, depth)

    @classmethod
    def _add_header(cls, value, depth):
        chain = cls.build_header_chain(depth)
        cls.cls_dict_markdown += chain.replace('value', value.title())

    @classmethod
    def _add_value(cls, key, value, depth):
        chain = cls.build_value_chain(key, value, depth)
        cls.cls_dict_markdown += chain

    @classmethod
    def build_header_chain(cls, depth):
        chain = cls.list_tag * (bool(depth)) + cls.htag * (depth + 1) + \
                ' value ' + (cls.htag * (depth + 1) + '\n')
        return chain

    @classmethod
    def build_value_chain(cls, key, value, depth):
        chain = cls.tab * (bool(depth - 1)) + cls.list_tag + \
                str(key) + ": " + str(value) + "\n"
        return chain
