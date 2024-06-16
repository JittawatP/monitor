import mysql.connector

def get_connection():
# ข้อมูลสำหรับเชื่อมต่อกับ MySQL
    return mysql.connector.connect(
            host = '',
            user = '',
            password = '',
            database = ''
    )
