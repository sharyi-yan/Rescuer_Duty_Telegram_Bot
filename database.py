import mysql.connector


def connect():
    mysqldb = mysql.connector.connect(
        host="your_host",
        user="name_user",
        password="your_password",
        port="your_port",
        database="name_of_database"
    )
    return mysqldb


db = connect()
cursor = db.cursor(buffered=True)
