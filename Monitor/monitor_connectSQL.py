import mysql.connector

# ข้อมูลสำหรับเชื่อมต่อกับ MySQL
db_config = {
       'host': '192.168.1.14',
       'user': 'Bank',
       'password': 'P@ssword1',
       'database': 'foamwebdev',
}

# เชื่อมต่อกับฐานข้อมูล
connection = mysql.connector.connect(**db_config)

# สร้าง Cursor เพื่อทำงานกับฐานข้อมูล
cursor = connection.cursor()

sql = "SELECT * FROM tblresult order by `sample#` desc limit 10;"
cursor.execute(sql)

# ดึงข้อมูล
#result = cursor.fetchall()
#for row in result:
#    print(row)

# ปิด Cursor และเชื่อมต่อฐานข้อมูล
cursor.close()
connection.close()

# สร้าง HTML จากข้อมูลที่ดึงมา
html_data = "<table>"
for row in result:
    html_data += "<tr>"
    for column in row:
        html_data += "<td>{}</td>".format(column)
    html_data += "</tr>"
html_data += "</table>"

# เขียนข้อมูล HTML ลงในไฟล์
with open("output.html", "w") as file:
    file.write(html_data)