from dataclasses import dataclass
from typing import Type, Dict

from injector import inject

from core_get.actions.action import Action
from core_get.options.options import Options


@inject
@dataclass
class ActionExecutor:

    action_types: Dict[Type[Options], Action]

    def execute_action(self, options: Options):
        action = self.action_types[type(options)]
        action.exec(options)
