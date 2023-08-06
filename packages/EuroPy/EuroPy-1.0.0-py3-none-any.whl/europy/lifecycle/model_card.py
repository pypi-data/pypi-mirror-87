import os, yaml, json
from datetime import datetime
from typing import List, Optional
from europy.lifecycle.markdowner import Markdown
from europy.lifecycle.model_details import ModelDetails


class ModelCard:
    def __init__(self, model_details: ModelDetails=ModelDetails(title="--"), parameters={}):
        self.model_details = model_details
        self.parameters = parameters

    def to_markdown(self, level=2):
        md = Markdown()
        md.add_header('Model Card', level)

        md += self.model_details.to_markdown(level=level+1)
        
        md.add_header('Parameters', level+1)

        #FIXME: params only support one level
        md_param_list = ''
        for title, param_set in self.parameters.items():
            md_param_list += f'* **{title}**\n'
            for param_name, param in param_set.items():
                md_param_list += f'\t* {param_name}: '
                if isinstance(param, list):
                    md_param_list += '\n'
                    for l in param:
                        md_param_list += f'\t\t* {l}\n'
                else:
                    md_param_list += f'{param}'
                md_param_list += '\n'

        md.add_md_content(md_param_list)

        return md
        