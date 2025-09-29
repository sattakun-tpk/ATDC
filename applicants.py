import sqlite3

conn = sqlite3.connect("applicants.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS applicants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    position TEXT NOT NULL,
    experience TEXT
)
""")
conn.commit()

print("👋 ยินดีต้อนรับสู่ระบบสมัครงานออนไลน์ บริษัท ProBig")

name = input("กรุณากรอกชื่อ: ")
age = int(input("กรุณากรอกอายุ: "))
position = input("ตำแหน่งที่สมัคร: ")
experience = input("ประสบการณ์ทำงาน: ")


if age < 18:
    print("ขออภัย คุณต้องมีอายุตั้งแต่ 18 ปีขึ้นไปจึงจะสมัครงานได้")
else:
    # บันทึกข้อมูลลงฐานข้อมูล
    cursor.execute(
        "INSERT INTO applicants (name, age, position, experience) VALUES (?, ?, ?, ?)",
        (name, age, position, experience)
    )
    conn.commit()

    print("บันทึกข้อมูลเรียบร้อย ขอบคุณที่สมัครงาน!")

# ปิดการเชื่อมต่อ
conn.close()
