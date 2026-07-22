"""
Strategy Loader
"""

import importlib
import config


def get_strategy():
    """
    根據 config 載入策略
    """

    module_name = f"strategies.{config.STRATEGY}"

    try:
        return importlib.import_module(module_name)

    except ModuleNotFoundError:
        raise ValueError(
            f"Strategy '{config.STRATEGY}' does not exist."
        )