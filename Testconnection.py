import mysql.connector
import schedule
import time
from datetime import datetime
# ข้อมูลสำหรับเชื่อมต่อกับ MySQL
db_config = {
       'host': '192.168.1.14',
       'user': 'Bank',
       'password': 'P@ssword1',
       'database': 'foamwebdev',
}

# ตำแหน่งของไฟล์ SQL
sql_file_path = r'D:\SQLscript\updateWebx.sql'

# เชื่อมต่อกับ MySQL
try:
    connection = mysql.connector.connect(**db_config)

    # ตรวจสอบว่าการเชื่อมต่อสำเร็จหรือไม่
    if connection.is_connected():
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("Connection to MySQL successful")

        # อ่านไฟล์ SQL
        with open(sql_file_path, 'r') as sql_file:
            sql_script = sql_file.read()

        # สร้าง Cursor เพื่อ execute คำสั่ง SQL
        cursor = connection.cursor()

        # Execute คำสั่ง SQL จากไฟล์
        cursor.execute(sql_script)

        # Commit การเปลี่ยนแปลง
        connection.commit()

        print(f"SQL processing successful {current_time}")

except mysql.connector.Error as err:
    print(f"Error occurred while connecting.: {err}")

finally:
    # ปิดการเชื่อมต่อ
    if 'connection' in locals() and connection.is_connected():
        connection.close()
        print("Closed connection to MySQL")

def run_sql_script():
    try:
        connection = mysql.connector.connect(**db_config)

        if connection.is_connected():
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print("Connection to MySQL successful")

            with open(sql_file_path, 'r') as sql_file:
                sql_script = sql_file.read()

            cursor = connection.cursor()
            cursor.execute(sql_script)
            connection.commit()

            print(f"SQL processing successful {current_time}")

    except mysql.connector.Error as err:
        print(f"Error occurred while connecting.: {err}")

    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("Closed connection to MySQL")

# กำหนดให้ run_sql_script ทำงานทุก 1 นาที
schedule.every(1).hours.do(run_sql_script)

# วนลูปเพื่อให้โปรแกรมทำงานตลอดเวลา
while True:
    schedule.run_pending()
    time.sleep(1)
