import mysql.connector


def connect():
    mysqldb = mysql.connector.connect(
        host="eu-cdbr-west-01.cleardb.com",
        user="bf967e1b7d5eb9",
        password="a78f16ed",
        port="3306",
        database="heroku_ace575c7c6b7834"
    )
    return mysqldb


db = connect()
cursor = db.cursor(buffered=True)
