import copy
import json
import logging
from typing import List, Tuple

from jinja2 import Environment, StrictUndefined

from pr_agent.algo.ai_handler import AiHandler
from pr_agent.algo.pr_processing import get_pr_diff, retry_with_fallback_models
from pr_agent.algo.token_handler import TokenHandler
from pr_agent.algo.utils import load_yaml
from pr_agent.config_loader import get_settings
from pr_agent.git_providers import get_git_provider
from pr_agent.git_providers.git_provider import get_main_pr_language
from pr_agent.tools.save_pr_info import get_pr_card_num, get_card_info, pr_other_info_write_json


class PRInformation:
    def __init__(self, pr_url: str, args: list = None):
        """
        Initialize the PRDescription object with the necessary attributes and objects for generating a PR description
        using an AI model.
        Args:
            pr_url (str): The URL of the pull request.
            args (list, optional): List of arguments passed to the PRDescription class. Defaults to None.
        """
        # Initialize the git provider and main PR language
        self.git_provider = get_git_provider()(pr_url)
        self.main_pr_language = get_main_pr_language(
            self.git_provider.get_languages(), self.git_provider.get_files()
        )
        self.pr_url = pr_url

        # Initialize the AI handler
        self.ai_handler = AiHandler()
    
        # Initialize the variables dictionary
        self.vars = {
            "title": self.git_provider.pr.title,
            "branch": self.git_provider.get_pr_branch(),
            "description": self.git_provider.get_pr_description(),
            "language": self.main_pr_language,
            "diff": "",  # empty diff for initial calculation
            "extra_instructions": get_settings().pr_description.extra_instructions,
            "commit_messages_str": self.git_provider.get_commit_messages()
        }

        self.contriutor_info = {
            "author":self.git_provider.get_author(),
            "reviewer":self.git_provider.get_pr_reviewer(),
        }

        self.user_description = self.git_provider.get_user_description()
        self.icafe_card = get_pr_card_num(self.vars['description'])
    
        # Initialize the token handler
        self.token_handler = TokenHandler(
            self.git_provider.pr,
            self.vars,
            get_settings().pr_description_prompt.system,
            get_settings().pr_description_prompt.user,
        )
    
        # Initialize patches_diff and prediction attributes
        self.patches_diff = None
        self.prediction = None

    async def run(self):
        """
        获取PR的信息,
        1. icafe信息,这里的icafe信息要包含父卡片相关信息
        2. PR 标题, PR的各个参与者, 更改的内容,以及各个commit信息
        3. 用于获取PR描述使用的prompts内容
        """
        logging.info('Display a PR Information')
        logging.info('PR url: ', self.pr_url)
        logging.info('Author: ', self.contriutor_info['author'])
        logging.info('Reviewer: ', self.contriutor_info['reviewer'])
        logging.info('Icafe info: ', self.icafe_card)
        pr_id = self.pr_url.split('/')[-1]
        if len(self.icafe_card) == 1:
            card_id = self.icafe_card[0].split('-')[-1]
            card_title, card_created_user, card_responsible_people, card_parent_info = get_card_info(card_id)
            file_name = "pr_icafe_info.json"
            pr_other_info_write_json(
                        file_name=file_name,
                        key = pr_id,             
                        card_title=card_title, 
                        card_created_user=card_created_user, 
                        card_responsible_people=card_responsible_people, 
                        card_parent_info=card_parent_info)
        
        # 将参与者的信息写入pr_contributor_info.json
        file_name = "pr_contributor_info.json"
        pr_other_info_write_json(
                    file_name=file_name,
                    key = pr_id,             
                    author=self.contriutor_info['author'],
                    reviewer=self.contriutor_info['reviewer'])
        
        return ""