import sqlite3

DB = "inventory.db"


def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS products(
        product_id    TEXT PRIMARY KEY,
        product_name  TEXT NOT NULL,
        quantity      INTEGER NOT NULL DEFAULT 0,
        price         REAL NOT NULL DEFAULT 0
    )
    """)
  
    sample = [
        ("P001", "ข้าวหอมมะลิ 5 กก.", 12, 199.0),
        ("P002", "ปลากระป๋อง",       0,  28.5),
        ("P003", "น้ำปลา 700 มล.",    7,  35.0),
        ("P004", "บะหมี่กึ่งสำเร็จรูป", 55, 6.0),
        ("P005", "ทิชชู่ม้วน",        2,  18.0),
    ]
    cur.executemany("""
        INSERT OR IGNORE INTO products(product_id, product_name, quantity, price)
        VALUES (?, ?, ?, ?)
    """, sample)
    conn.commit()
    return conn, cur



def search_product(cur, keyword: str):
    
    cur.execute("""
        SELECT product_id, product_name, quantity, price
        FROM products
        WHERE lower(product_name) LIKE '%' || lower(?) || '%'
        ORDER BY product_name
    """, (keyword,))
    return cur.fetchall()


def chatbot():
    print("🏪 SaraKlong6 | ระบบตรวจสอบสต๊อกสินค้า")
    conn, cur = init_db()

    keyword = input("พิมพ์ชื่อสินค้าที่ต้องการตรวจสอบ: ").strip()
    rows = search_product(cur, keyword)

  
    if not rows:
        print("ไม่พบสินค้าที่ตรงกับคำค้น กรุณาลองใหม่")
        conn.close()
        return

   
    for pid, name, qty, price in rows:
        if qty == 0:
            print(f" {name} (รหัส {pid}) : สินค้าหมด")
        elif qty <= 5:
            print(f" {name} (รหัส {pid}) : คงเหลือ {qty} ชิ้น | ราคา {price:.2f} บาท/ชิ้น (ใกล้หมด)")
        else:
            print(f" {name} (รหัส {pid}) : คงเหลือ {qty} ชิ้น | ราคา {price:.2f} บาท/ชิ้น")

    conn.close()


if __name__ == "__main__":
    init_db()
    chatbot()
