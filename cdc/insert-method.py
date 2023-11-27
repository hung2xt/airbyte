import pymysql
from pymysqlreplication import BinLogStreamReader
from pymysqlreplication.row_event import DeleteRowsEvent, UpdateRowsEvent, WriteRowsEvent
from google.cloud import bigquery

mysql_settings = {
    "host": "172.17.0.2",
    "port": 3306,
    "user": "root",
    "passwd": "asd@1234"
}

# Connect to the MySQL server
connection = pymysql.connect(**mysql_settings)
client = bigquery.Client()
# Stream the binary logs
stream = BinLogStreamReader(
    connection_settings = mysql_settings,
    server_id=100,
    only_events=[DeleteRowsEvent, WriteRowsEvent, UpdateRowsEvent],
    blocking=True
)

try:
    with connection.cursor() as cursor:
        cursor.execute("DESCRIBE classicmodels.customers")
        result = cursor.fetchall()
        schema = {f"UNKNOWN_COL{i}": column[0] for i, column in enumerate(result)}
finally:
    connection.close()

def insert_into_bigquery(data, table_id):
    errors = client.insert_rows_json(table_id, [data])
    if errors != []:
        print(f"Errors: {errors}")

def transform_data(row_data):
    return {
        "customerNumber": row_data["UNKNOWN_COL0"],
        "customerName": row_data["UNKNOWN_COL1"],
        "contactLastName": row_data["UNKNOWN_COL2"],
        "contactFirstName": row_data["UNKNOWN_COL3"],
        "phone": row_data["UNKNOWN_COL4"],
        "addressLine1": row_data["UNKNOWN_COL5"],
        "addressLine2": row_data["UNKNOWN_COL6"],
        "city": row_data["UNKNOWN_COL7"],
        "state": row_data["UNKNOWN_COL8"],
        "postalCode": row_data["UNKNOWN_COL9"],
        "country": row_data["UNKNOWN_COL10"],
        "salesRepEmployeeNumber": row_data["UNKNOWN_COL11"],
        "creditLimit": float(row_data["UNKNOWN_COL12"])  # Assuming Decimal type needs to be converted to float
    }

try:
    for binlogevent in stream:
        if isinstance(binlogevent, WriteRowsEvent) and binlogevent.table == "customers":
            for row in binlogevent.rows:
                event = {"data": row["values"]}
                transformed_data = transform_data(event['data'])
                # Define BigQuery table ID
                table_id = "classicmodel_customers"
                insert_into_bigquery(transformed_data, table_id)
                print(transformed_data)
finally:
    stream.close()


