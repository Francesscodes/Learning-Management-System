try:
    import importlib
    mysql_connector = importlib.import_module("mysql.connector")
except ImportError as error:
    raise ImportError(
        "mysql-connector-python is not installed. Install it with 'pip install mysql-connector-python'."
    ) from error

db = mysql_connector.connect(
    host="localhost",
    user="root",
    password="anselemngo97$",
    database="LMS_DB"
)

cursor = db.cursor()