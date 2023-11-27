import pymysql
from pymysqlreplication import BinLogStreamReader
from pymysqlreplication.row_event import DeleteRowsEvent, UpdateRowsEvent, WriteRowsEvent

mysql_settings = {
    "host": "172.17.0.2",
    "port": 3306,
    "user": "root",
    "passwd": "asd@1234"
}

# Connect to the MySQL server
connection = pymysql.connect(**mysql_settings)

# Stream the binary logs
stream = BinLogStreamReader(
    connection_settings = mysql_settings,
    server_id=100,
    only_events=[DeleteRowsEvent, WriteRowsEvent, UpdateRowsEvent],
    blocking=True
)

try:
    for binlogevent in stream:
        for row in binlogevent.rows:
            event = {"schema": binlogevent.schema, "table": binlogevent.table}

            if isinstance(binlogevent, DeleteRowsEvent):
                event["action"] = "delete"
                event["data"] = row["values"]
            elif isinstance(binlogevent, UpdateRowsEvent):
                event["action"] = "update"
                event["before_values"] = row["before_values"]
                event["after_values"] = row["after_values"]
            elif isinstance(binlogevent, WriteRowsEvent):
                event["action"] = "insert"
                event["data"] = row["values"]

            print(event)

finally:
    stream.close()


