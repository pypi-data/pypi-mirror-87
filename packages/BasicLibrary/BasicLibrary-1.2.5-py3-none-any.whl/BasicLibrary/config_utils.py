import configparser

class ConfigUtils:
    '''
    读取配置文件数据的底层方法
    '''
    def __init__(self, config_path):
        self.cfg = configparser.ConfigParser()
        self.cfg.read(config_path)

    def read_value(self,section,key):
        '''
        :param section: 配置中[]内的值
        :param key: 配置中值的key
        :return: 值的value
        Examples:
        参数 ConfigUtils(config_path).read_value('sit.mysql.users','database')
        返回 users  字符串数据类型
        '''
        value = self.cfg.get(section,key)
        return value

    def read_items(self,section):
        '''
        :param section: 配置中[]内的值
        :return: {'':'','':'','':'','':''} 字典数据类型
        Examples:
        参数 ConfigUtils(config_path).read_items('sit.mysql.users')
        '''
        items = self.cfg.items(section)
        dict = {}
        for i in range(len(items)):
            if items[i][0] != 'port':
                dict[items[i][0]] = items[i][1]
            else:
                dict[items[i][0]] = int(items[i][1])
        return dict