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
from pr_agent.tools.save_pr_info import save_pr_info, save_pr_info_json, get_pr_card_num, get_card_info


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
            "reviwer":self.git_provider.get_pr_reviewer(),
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

        # logging.debug("self.vars: %s", self.vars)
        # logging.debug("self.token_handler: %s", self.token_handler)
        # for k,v in self.vars.items():
        #     print("k: %s, v: %s" %(k,v))
        #     print("#"*88)

        print(self.contriutor_info)
        print(self.icafe_card)
        return ""