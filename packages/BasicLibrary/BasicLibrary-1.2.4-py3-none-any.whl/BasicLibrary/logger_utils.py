'''
Documentation: 日志文件
引用包名是：BasicLibrary   引用本python文件，请使用 from BasicLibrary.logger_utils import logger
日志按日生成，名称是：xxxx_xx_xxApiTest.log
找到LogManager('xxx').get_logger_and_add_handlers()方法，log_path='../../pythonlogs', 可以指定日志生成路径
关掉调整颜色的提示：
    在生成的nb_log_config.py，找到32、33行，修改成如下：
    AUTO_PATCH_PRINT = True  # 是否自动打print的猴子补丁，如果打了后指不定，print自动变色和可点击跳转。
    WARNING_PYCHARM_COLOR_SETINGS = False
'''

import time
from nb_log import LogManager

now_time = time.strftime('%Y_%m_%d')
logger = LogManager().get_logger_and_add_handlers(log_filename=now_time+'ApiTest.log')