# coding=utf-8

import os
import warnings
from configparser import ConfigParser

ROOT_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__),os.pardir))
CONFIG_FILE_PATH = os.path.join(ROOT_PATH,'config.cfg')

class Config():
    def __init__(self) -> None:
        try:
            os.path.exists(CONFIG_FILE_PATH)
        except FileNotFoundError as e:
            warnings.warn(f'{e}\n 未找到 config.cfg 配置文件，请在根目录下创建配置文件！')
        except Exception as e:
            warnings.warn(f'{e}\n 读取 config.cfg 配置错误，请检查或重新配置！')

    def get_config(self,section) -> dict:
        # 读取本地配置文件
        config = ConfigParser()
        config.read(CONFIG_FILE_PATH,encoding='utf-8')

        if config.has_section(section):
            config_dict = dict(config.items(section))
        else:
            warnings.warn(f'\n 在 config.cfg 配置文件，未找到配置项！')
            config_dict = {}

        return config_dict