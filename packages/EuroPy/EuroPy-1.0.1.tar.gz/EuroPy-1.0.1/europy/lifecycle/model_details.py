import os, yaml, json
from datetime import datetime
from typing import List, Optional
from europy.lifecycle.markdowner import Markdown

class ModelDetails:
    def __init__(self, title: str,
            organization: Optional[str]=None,
            authors: List[str]=[],
            emails: List[str]=[],
            model_date: datetime=datetime.now(),
            model_version: str='--',
            citation_details: str='--',
            model_license: str='--',
            model_url: str='--',
            data_license: str='--',
            data_url: str='--',
            description: str='--'):
        """[summary]

        Args:
            title (str): Title of the model card
            organization (Optional[str], optional): Organization or company developing the model. Defaults to None.
            authors (List[str], optional): list of author names. Defaults to [].
            emails (List[str], optional): list of author email (mapped to authors). Defaults to [].
            model_date (datetime, optional): date of the model publication. Defaults to datetime.now().
            model_version (str, optional): version of the model. Defaults to '--'.
            citation_details (str, optional): how to cite the model (e.g. BibTex). Defaults to '--'.
            model_license (str, optional): license associated with the model code. Defaults to '--'.
            model_url (str, optional): url associated with the model code. Defaults to '--'.
            data_license (str, optional): license associated with the model's data: Defaults to '--'.
            data_url: (str, optional): url associated with the model's data. Defaults to '--'.
            description (str, optional): . Defaults to '--'.
        """

        self.title = title
        self.organization = organization
        self.authors = authors
        self.emails = emails
        self.model_date = model_date
        self.model_version = model_version
        self.citation_details = citation_details
        
        self.model_license = model_license
        self.model_url = model_url

        self.data_license = data_license
        self.data_url = data_url
        
        self.description = description 
    
    def to_markdown(self, level: int=3) -> Markdown:
        md = Markdown()
        md.add_header('Model Details', level)
        # md.add_dict_content(self.__dict__)

        md.add_md_content(f'**Organization**: {self.organization}')
        
        md.add_md_content(f'**Authors**:')
        author_content = ''
        for i, author in enumerate(self.authors):
            author_content += f'* {author} ({self.emails[i]})\n'

        md.add_md_content(author_content)

        md.add_md_content(f'**Created Date**: {self.model_date}')
        md.add_md_content(f'**Version**: {self.model_version}')
        md.add_md_content(f'**Citation**: \n```\n{self.citation_details}\n```')
        md.add_md_content(f'**Model License**: {self.model_license}')
        md.add_md_content(f'**Model URL**: {self.model_url}')
        md.add_md_content(f'**Data License**: {self.data_license}')
        md.add_md_content(f'**Data URL**: {self.data_url}')
        
        md.add_md_content(f'**Description**:')
        md.add_md_content(self.description)
        return md

    @classmethod
    def of(cls, file_path: str):
        if file_path:
            # load the model detail path
            with open(file_path, 'r') as f:
                # load in yml or json format (to dict)
                if os.path.split(file_path)[-1].split('.')[-1] in ["yml", "yaml"]:
                    details_data = yaml.load(f, Loader=yaml.FullLoader)
                else:
                    details_data = json.load(f)

                details = cls(**details_data)
                return details
        return