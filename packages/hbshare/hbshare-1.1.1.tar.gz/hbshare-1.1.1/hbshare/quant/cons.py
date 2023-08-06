hb_ip = '192.168.223.152'

sql_user_hb = {
    'ip': hb_ip,
    'user': 'readonly',
    'pass': 'c24mg2e6',
    'port': '3306'
}

sql_write_path_hb = {
    'commodities':
        'mysql+mysqldb://%s:%s@%s:%s/commodities?charset=utf8'
        % (sql_user_hb['user'], sql_user_hb['pass'], hb_ip, sql_user_hb['port']),
    'stocks':
        'mysql+mysqldb://%s:%s@%s:%s/stocks?charset=utf8'
        % (sql_user_hb['user'], sql_user_hb['pass'], hb_ip, sql_user_hb['port']),
    'work':
        'mysql+mysqldb://%s:%s@%s:%s/work?charset=utf8'
        % (sql_user_hb['user'], sql_user_hb['pass'], hb_ip, sql_user_hb['port']),
    'daily':
        'mysql+mysqldb://%s:%s@%s:%s/daily_data?charset=utf8'
        % (sql_user_hb['user'], sql_user_hb['pass'], hb_ip, sql_user_hb['port']),
}
