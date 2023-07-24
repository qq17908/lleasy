# coding=utf-8
import logging

class Log():
    def __init__(self,name) -> None:
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level=logging.DEBUG)

        self.formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(module)s - %(levelname)s: %(message)s')
        # 文件输出
        self.file_handler = logging.FileHandler('lleasy.log')
        self.file_handler.setLevel(level=logging.INFO)
        self.file_handler.setFormatter(self.formatter)

        # 屏幕输出
        self.stream_handler = logging.StreamHandler()
        self.stream_handler.setLevel(logging.DEBUG)
        self.stream_handler.setFormatter(self.formatter)

        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(self.stream_handler)

    def info(self,message) -> None:
        self.logger.info(message)

    def warning(self,message) -> None:
        self.logger.warning(message)
    
    def error(self,message) -> None:
        self.logger.error(message)
    
    def critical(self, message) -> None:
        self.logger.error(message)
