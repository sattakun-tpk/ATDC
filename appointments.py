import sqlite3
from datetime import datetime, date

DB = "promotion.db"

def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS promotions(
        promo_id    INTEGER PRIMARY KEY AUTOINCREMENT,
        title       TEXT NOT NULL,
        description TEXT NOT NULL,
        start_date  TEXT NOT NULL,   -- เก็บเป็น ISO: YYYY-MM-DD
        end_date    TEXT NOT NULL
    )
    """)

    sample = [
        ("ปีใหม่ลดแรง 50%", "ลดทันที 50% สินค้าที่ร่วมรายการ", "2025-12-25", "2026-01-05"),
        ("คูปองของขวัญ 300", "รับคูปอง 300 บาท เมื่อซื้อครบ 1,500", "2025-12-20", "2026-01-10"),
        ("ช้อปข้ามปี", "ส่งฟรีทุกออเดอร์ช่วงเคาท์ดาวน์", "2025-12-31", "2026-01-01"),
    ]
    cur.executemany("""
        INSERT OR IGNORE INTO promotions(promo_id, title, description, start_date, end_date)
        VALUES(NULL, ?, ?, ?, ?)
    """, sample)
    conn.commit()
    return conn, cur


def parse_date(s: str) -> date | None:
    """รองรับหลายรูปแบบ: YYYY-MM-DD, DD/MM/YYYY, DD-MM-YYYY"""
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
        try:
            return datetime.strptime(s.strip(), fmt).date()
        except ValueError:
            pass
    return None


def is_active_on(check: date, start_s: str, end_s: str) -> bool:
    start = datetime.strptime(start_s, "%Y-%m-%d").date()
    end = datetime.strptime(end_s, "%Y-%m-%d").date()
    return start <= check <= end


def show_promo_row(row):
    pid, title, desc, start_s, end_s = row
    
    msg = (
        f"🎉 โปรโมชัน: {title}\n"
        f"รายละเอียด: {desc}\n"
        f"ช่วงเวลา: {start_s} ถึง {end_s}"
    )
    print(msg)



def chatbot():
    print("🎊 ระบบส่งเสริมการตลาดช่วงปีใหม่ (บริษัท ABC)")
    print("พิมพ์ 1 เพื่อค้นหาด้วย 'ชื่อโปรโมชัน'")
    print("พิมพ์ 2 เพื่อค้นหาด้วย 'วันที่' (โปรที่มีผลในวันนั้น)")
    choice = input("เลือก (1/2): ").strip()

    conn, cur = init_db()

    if choice == "1":
        title = input("พิมพ์ชื่อโปรโมชัน: ").strip()
        cur.execute("""
            SELECT promo_id, title, description, start_date, end_date
            FROM promotions WHERE lower(title)=lower(?)
        """, (title,))
        row = cur.fetchone()
        if not row:
            print("ไม่พบโปรโมชันชื่อนี้ในระบบ")
            conn.close()
            return

        
        today = date.today()
        start = datetime.strptime(row[3], "%Y-%m-%d").date()
        end = datetime.strptime(row[4], "%Y-%m-%d").date()

        if today < start:
            print(f"โปรโมชันยังไม่เริ่ม (เริ่ม {row[3]})")
        elif today > end:
            print(f"โปรโมชันหมดเขตแล้ว (หมดเขต {row[4]})")
        else:
            show_promo_row(row)
            print("✅ สถานะ: ใช้งานได้วันนี้")

    elif choice == "2":
        s = input("กรอกวันที่ (เช่น 2025-12-31 หรือ 31/12/2025): ")
        d = parse_date(s)
        if not d:
            print("รูปแบบวันที่ไม่ถูกต้อง")
            conn.close()
            return

        cur.execute("SELECT promo_id, title, description, start_date, end_date FROM promotions")
        rows = cur.fetchall()
        active = [r for r in rows if is_active_on(d, r[3], r[4])]
        if not active:
            
            print("ไม่มีโปรโมชันที่ใช้งานได้ในวันดังกล่าว")
        else:
            print(f"โปรโมชันที่ใช้งานได้ในวันที่ {d.isoformat()}:")
            for r in active:
                show_promo_row(r)
                print("-" * 40)
    else:
        print("ตัวเลือกไม่ถูกต้อง (ต้องเป็น 1 หรือ 2)")

    conn.close()


if __name__ == "__main__":
    init_db()
    chatbot()
