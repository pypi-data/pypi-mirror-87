from .BaseFunc import get_conf
import GeneralSQL

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
    # t.set_sql('show tables')
    t.set_sql('desc class')
    t.get_data()
    res = t.get_format_data()
    print(res)
    t.close()

if __name__ == "__main__":
    main()