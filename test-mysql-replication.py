from pymysqlreplication import BinLogStreamReader

mysql_settings = {'host': '172.17.0.2', 'port': 3306, 'user': 'root', 'passwd': 'asd@1234'}

stream = BinLogStreamReader(connection_settings = mysql_settings, server_id=100)

for binlogevent in stream:
    binlogevent.dump()

stream.close()

