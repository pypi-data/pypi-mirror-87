import configparser

def get_conf(path):
    """
    获取 conf 配置文件信息

    path: 配置文件路径
    """
    conf = configparser.RawConfigParser()
    conf.read(path)
    conf_dic = {s: dict(conf.items(s)) for s in conf.sections()}
    del conf
    return conf_dic
