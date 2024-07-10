import mysql.connector

def get_connection():
# ข้อมูลสำหรับเชื่อมต่อกับ MySQL
    return mysql.connector.connect(
            host = '192.168.1.14',
            user = 'Bank',
            password = 'P@ssword1',
            database = 'foamwebdev'
    )