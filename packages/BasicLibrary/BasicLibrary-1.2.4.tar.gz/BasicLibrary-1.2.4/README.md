关于nb_log模块：
1、如果是mac电脑，找到LogManager('xxx').get_logger_and_add_handlers()方法
2、修改log_path='../../pythonlogs',看项目路径要放到哪里
3、调整日志颜色：
    1)使用pycharm时候，建议重新自定义设置pycharm的console里面的主题颜色。
    设置方式为 打开pycharm的 file -> settings -> Editor -> Color Scheme -> Console Colors 选择monokai，
    并重新修改自定义6个颜色，设置Blue为1585FF，Cyan为06B8B8，Green 为 05A53F，Magenta为 ff1cd5,red为FF0207，yellow为FFB009。
    2)使用xshell或finashell工具连接linux也可以自定义主题颜色，默认使用shell连接工具的颜色也可以。
    颜色效果如连接 https://i.niupic.com/images/2020/03/24/76zi.png
4、关掉调整颜色的提示
    在生成的nb_log_config.py，找到32、33行，修改成如下：
    AUTO_PATCH_PRINT = True  # 是否自动打print的猴子补丁，如果打了后指不定，print自动变色和可点击跳转。
    WARNING_PYCHARM_COLOR_SETINGS = False
