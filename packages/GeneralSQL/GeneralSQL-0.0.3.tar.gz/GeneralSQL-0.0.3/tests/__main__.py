from .BaseFunc import get_conf
import GeneralSQL

def select_test(t):
    """
    查询数据测试
    """
    col = ['class_id', 'class_name', 'class_grade', 'class_type', 'class_create_time']
    t.Sel('class', *col)
    print(t.get_sql())
    t.get_data()
    res = t.get_format_data()
    return res

def delete_test(t):
    """
    删除数据测试
    """
    t.Del('class')
    t.get_func_sql('del')
    print(t.get_sql())
    t.get_data()
    res = t.get_format_data()
    t.rollback()
    return res

def update_test(t):
    """
    更新语句测试
    """
    up_data = {
        'class_grade': '初一'
    }
    t.Up('class', **up_data)
    t.get_func_sql('up')
    print(t.get_sql())
    t.get_data()
    res = t.get_format_data()
    t.commit()
    return res

def insert_test(t):
    """
    添加数据测试
    """
    col = ['class_name', 'class_grade', 'class_type']
    add_data = [
        {'class_name': '1班', 'class_grade': '初一', 'class_type': '中学'},
        {'class_name': '2班', 'class_grade': '初一', 'class_type': '中学'},
        {'class_name': '3班', 'class_grade': '初一', 'class_type': '中学'}
    ]
    t.Add('class', col, add_data)
    t.get_func_sql('add')
    print(t.get_sql_list())
    res = t.get_insert_data()
    # t.rollback()
    t.commit()
    return res

def base_test(t):
    """
    基本语句测试
    """
    t.set_sql('show tables')
    t.set_sql('desc class')
    t.get_data()
    res = t.get_format_data()
    return res

def main():
    """
    测试主进程
    """
    conf = get_conf('tests/conf.ini')
    db_info = {
        'database': conf['db_mysql_conf']['db'],
        'user': conf['db_mysql_conf']['username'],
        'password': conf['db_mysql_conf']['password'],
        'host': conf['db_mysql_conf']['host'],
    }
    t = GeneralSQL.SeniorSQL()
    t.set_db_info(**db_info)
    # 基本语句测试
    base_test(t)
    # 添加数据测试
    # print(insert_test(t))
    # 更新数据测试
    # print(update_test(t))
    # 删除数据测试
    # print(delete_test(t))
    # 查询数据测试
    print(select_test(t))
    t.close()

if __name__ == "__main__":
    main()