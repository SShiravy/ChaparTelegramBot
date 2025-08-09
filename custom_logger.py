import logging
from logging.handlers import RotatingFileHandler
import colorlog

class ConfigRootLogger:
    __instance = None

    def __new__(cls,consol_log:bool=True,consol_log_level=logging.DEBUG,
                log_file:bool=False,file_log_level=logging.DEBUG,file_log_name:str="app",
                timing:bool=True):

        if cls.__instance is None:
            cls.__instance = logging.getLogger()
            cls.__instance.setLevel(logging.DEBUG)
            if consol_log:
                cls.__instance.addHandler(cls.__consol_handler(consol_log_level))
            if log_file:
                cls.__instance.addHandler(cls.__file_handler(file_log_level,file_log_name))
        return cls.__instance

    @classmethod
    def __consol_handler(cls,log_level):
        formatter = colorlog.ColoredFormatter(
            '{log_color}#{asctime}#{filename}# --*{levelname}*->|[{message}]|',
            style='{',
            datefmt='%H:%M:%S"',
            log_colors={
                'DEBUG': 'bg_white',
                'INFO': 'cyan',
                'WARNING': 'yellow',
                'ERROR': 'bold_red',
                'CRITICAL': 'bold_purple',
            }
        )
        consol_handler = logging.StreamHandler()
        consol_handler.setFormatter(formatter)
        consol_handler.setLevel(log_level)
        return consol_handler


    @classmethod
    def __file_handler(cls,log_level,file_log_name:str):
        file_formatter = logging.Formatter(
            '#{asctime}#{filename}# --*{levelname}*->|[{message}]|',
               style='{',
               datefmt='%D;%H:%M:%S"')
        file_handler = RotatingFileHandler(filename=f'{file_log_name}.log', mode='a', encoding="utf-8",
                                           maxBytes=int(1e6), backupCount=1)
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(log_level)
        return file_handler

logger = ConfigRootLogger(consol_log_level=logging.WARNING,log_file=True, file_log_level=logging.INFO)

if __name__ == '__main__':
    ConfigRootLogger().debug('mio')
    ConfigRootLogger().info('mio')
    ConfigRootLogger().warning('mio')
    ConfigRootLogger().error('mio')
    ConfigRootLogger().critical('mio')
    ConfigRootLogger().exception('mio')