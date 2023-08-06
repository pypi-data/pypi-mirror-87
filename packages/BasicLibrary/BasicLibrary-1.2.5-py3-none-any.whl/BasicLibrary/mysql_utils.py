'''
Documentation: 查询操作mysql数据库的。
引用包名是：BasicLibrary   引用本python文件，请使用 from BasicLibrary.mysql_utils import *
'''

import pymysql
from BasicLibrary.logger_utils import logger

def __get_mysql_connection_with_config(config):
    try:
        # logger.info('数据库链接'+str(config))
        if config.get('charset') is None:
            config['charset'] = 'utf8'
        connect = pymysql.connect(**config)
        return connect
    except pymysql.OperationalError as e:
        logger.error('数据库连接失败，原因：%s' % e)
        raise AssertionError('数据库连接失败，原因：%s' % e)
    except pymysql.MySQLError as e:
        logger.error('数据库连接失败，原因：%s' % e)
        raise AssertionError('数据库连接失败，原因：%s' % e)
    except Exception as e:
        logger.error('数据库连接失败，原因：%s' % e)
        raise AssertionError('数据库连接失败，原因：%s' % e)

def __query_one(con,sql):
    '''
        查询一条数据。返回字典。
       【conn】:Connection类型，数据库连接
       【sql】: String类型，执行的sql
        RETURN: 字典类型

        Examples:
            |       方法     |      参数     |  参数  |
            | __query_one   |  <Connection> | <sql> |
        '''
    cur = con.cursor()
    try:
        logger.info('\n数据库执行SQL：'+ sql)
        cur.execute(sql)
        result = cur.fetchone()
        fields_list = []
        for field in cur.description:
            fields_list.append(field[0])
        con.commit()
        result_dict = {}
        if result is None or len(result) == 0:
            logger.info("数据库返回结果: None")
            return None
        for index in range(len(result)):
            result_dict[fields_list[index]] = result[index]
        logger.info("数据库返回结果: " + str(result_dict))
        return result_dict
    except pymysql.MySQLError as e:
        con.rollback()  # 若出错了，则回滚
        logger.error("数据库错误: " + e)
        raise AssertionError("数据库错误: " + e)

    finally:
        try:
            cur.close()
        except pymysql.MySQLError as e:
            logger.error("关闭cursor出错: " + e)
        except pymysql.OperationalError as e:
            logger.error("关闭cursor出错: " + e)
        try:
            con.close()
        except pymysql.MySQLError as e:
            logger.error("关闭数据库连接出错: " + e)
        except pymysql.OperationalError as e:
            logger.error("关闭数据库连接出错: " + e)

def __query_all(con,sql):
    '''
        查询所有数据。返回嵌套字典的列表。
       【conn】:Connection类型，数据库连接
       【sql】: String类型，执行的sql
        RETURN: 列表，列表里嵌套字典

        Examples:
            |    方法        |      参数     |  参数  |
            | __query_all   |  <Connection> | <sql> |
        '''
    cur = con.cursor()
    try:
        logger.info("\n数据库执行SQL: " + sql)
        cur.execute(sql)
        result = cur.fetchall()
        fields_list = []
        for field in cur.description:
            fields_list.append(field[0])
        con.commit()
        if result is None or len(result) == 0:
            logger.info("数据库返回结果: None")
            return None
        result_list = []
        for i in range(len(result)):
            row_dict = {}
            row = result[i]
            for j in range(len(row)):
                row_dict[fields_list[j]] = row[j]
            result_list.append(row_dict)
        logger.info("数据库返回结果: " + str(result_list))
        return result_list
    except pymysql.MySQLError as e:
        con.rollback()  # 若出错了，则回滚
        logger.error("数据库错误: " + e)
        raise AssertionError("数据库错误: " + e)

    finally:
        try:
            cur.close()
        except pymysql.MySQLError as e:
            logger.error("关闭cursor出错: " + e)
        except pymysql.OperationalError as e:
            logger.error("关闭cursor出错: " + e)
        try:
            con.close()
        except pymysql.MySQLError as e:
            logger.error("关闭数据库连接出错: " + e)
        except pymysql.OperationalError as e:
            logger.error("关闭数据库连接出错: " + e)

def __execute_sql(con,sql):
    '''
    操作数据库数据。
   【con】:Connection类型，数据库连接,
   【sql】: String类型，执行的sql,
    RETURN: Int类型，影响数据库数据行数.

    Examples:
        | 方法             |      参数      |  参数 |
        | __execute_sql    |  <Connection>  | <sql> |
    '''
    cur = con.cursor()
    try:
        logger.info('\n数据库执行SQL：'+ sql)
        cur.execute(sql)
        con.commit()
    except pymysql.MySQLError as e:
        con.rollback()  # 若出错了，则回滚
        logger.error("数据库错误: " + e)
        raise AssertionError("数据库错误: " + e)
    finally:
        try:
            cur.close()
        except pymysql.MySQLError as e:
            logger.error("关闭cursor出错: " + e)
        except pymysql.OperationalError as e:
            logger.error("关闭cursor出错: " + e)
        try:
            con.close()
        except pymysql.MySQLError as e:
            logger.error("关闭数据库连接出错: " + e)
        except pymysql.OperationalError as e:
            logger.error("关闭数据库连接出错: " + e)

def excute_mysql_sql_with_mysql(config,sql):
    '''
    数据库的删除、修改调用此方法
    :param config: 字典类型,含有host,port,user,password,db等信息的配置
    :param sql: String类型,sql语句
    :return: 空

    Examples:
        |   方法                      |          参数                                                                                             |   参数
        | excute_mysql_sql_with_mysql | {"host":"127.0.0.1","port":3306,"user":"root","password":"password","db":"database","charset":"utf8mb4"} |   <sql>
    '''
    con = __get_mysql_connection_with_config(config)
    return __execute_sql(con,sql)

def query_one_with_config(config,sql):
    '''
    查询一条数据调用此方法，如果有多条数据，查询出来的是最老的一条
    :param config: 字典类型,含有host,port,user,password,db等信息的配置
    :param sql: String类型,sql语句
    :return: {'':''} 字典数据格式

    Examples:
        |   方法                 |          参数                                                                                            |   参数
        | query_one_with_config | {"host":"127.0.0.1","port":3306,"user":"root","password":"password","db":"database","charset":"utf8mb4"} |   <sql>
    '''
    con = __get_mysql_connection_with_config(config)
    return __query_one(con,sql)

def query_all_with_config(config,sql):
    '''
    查询多条数据调用此方法
    :param config: 字典类型,含有host,port,user,password,db等信息的配置
    :param sql: String类型,sql语句
    :return:[{'':''},{'':''}] 列表数据格式

    Examples:
        |   方法                 |          参数                                                                                            |   参数
        | query_all_with_config | {"host":"127.0.0.1","port":3306,"user":"root","password":"password","db":"database","charset":"utf8mb4"} |   <sql>
    '''
    con = __get_mysql_connection_with_config(config)
    return __query_all(con, sql)

def get_define_data_by_field(config,sql,field):
    '''
    先查询出所有数据，再根据传入的field返回该字段对应的所有值，例如一个表有多条订单，传入订单号字段返回所有订单号的LIST
    :param config: config: 字典类型，含有host,port,user,password,db等信息的配置
    :param sql: String类型,sql语句
    :param field: String类型,想要获取的字段，例如order_no
    :return: [] 列表数据类型

    Examples:
        |   方法                    |          参数                                                                                            |   参数    | 参数
        | get_define_data_by_field | {"host":"127.0.0.1","port":3306,"user":"root","password":"password","db":"database","charset":"utf8mb4"} |   <sql>  |  <field>
    '''
    database_data = query_all_with_config(config, sql)
    field_list = []
    try:
        for i in range(len(database_data)):
            if field not in database_data[i].keys():
                logger.error('field【%s】不存在，请检查！' % field)
                break
            else:
                field_list.append(database_data[i].get(field))
        return field_list
    except TypeError:
        logger.info('查询到的数据为空')
        return field_list
    except Exception as e:
        logger.error('根据field查询报错啦，原因是：%' + e)
        return field_list
