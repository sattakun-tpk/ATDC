import sqlite3

DB_NAME = "campaign.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        customer_id     TEXT PRIMARY KEY,
        name            TEXT NOT NULL,
        campaign_eligible TEXT NOT NULL CHECK (campaign_eligible IN ('Yes','No')),
        balance         REAL NOT NULL DEFAULT 0
    )
    """)

    sample = [
        ("C001", "สมชาย ใจดี",       "Yes", 1200.00),
        ("C002", "สมหญิง แสนดี",     "No",   850.50),
        ("C003", "วีระพล ทองแท้",    "Yes",  90.00),
        ("C004", "ราตรี ศรีสมบูรณ์", "No",  500.00),
    ]
    cur.executemany(
        "INSERT OR IGNORE INTO customers(customer_id, name, campaign_eligible, balance) VALUES(?,?,?,?)",
        sample
    )
    conn.commit()
    return conn, cur


def find_customer(cur, mode: str, value: str):
    if mode == "id":
        cur.execute("SELECT customer_id, name, campaign_eligible, balance FROM customers WHERE customer_id = ?", (value,))
        return cur.fetchone()
    elif mode == "name":
        cur.execute(
            "SELECT customer_id, name, campaign_eligible, balance FROM customers WHERE lower(name) = lower(?)",
            (value,)
        )
        return cur.fetchone()
    return None


def show_customer(cus):
    cid, name, eligible, balance = cus
    print(f"\nพบลูกค้า: [{cid}] {name}")
    print(f"สิทธิ์คนละครึ่ง: {eligible}")
    print(f"ยอดเงินคงเหลือ (สมมติ): {balance:,.2f} บาท")

def chatbot():
    print("🛒 แคมเปญ \"คนละครึ่ง\" สำหรับลูกค้า ร้านค้า Big4")
    print("พิมพ์ 1 เพื่อตรวจด้วย customer_id  |  พิมพ์ 2 เพื่อตรวจด้วยชื่อ")
    choice = input("เลือกวิธีค้นหา (1/2): ").strip()

    if choice == "1":
        mode = "id"
        value = input("กรอก customer_id: ").strip()
    elif choice == "2":
        mode = "name"
        value = input("กรอกชื่อ-นามสกุลให้ตรง: ").strip()
    else:
        print("รูปแบบคำสั่งไม่ถูกต้อง (ต้องเป็น 1 หรือ 2)")
        return

    conn, cur = init_db()
    customer = find_customer(cur, mode, value)

    if customer is None:
        print("ไม่พบบัญชีลูกค้าในระบบ กรุณาตรวจสอบอีกครั้ง")
        conn.close()
        return

    show_customer(customer)
    cid, name, eligible, balance = customer

    if eligible == "Yes":
        try:
            amount = float(input("\nกรอกยอดซื้อสินค้า (บาท): ").strip())
            if amount <= 0:
                print("ยอดซื้อจะต้องมากกว่า 0 บาท")
            else:
                discount = amount * 0.50
                pay = amount - discount
                print(f"\n สิทธิ์ผ่าน: คุณ {name} ได้รับส่วนลดคนละครึ่ง 50% = {discount:,.2f} บาท")
                print(f"ยอดที่ต้องชำระหลังหักส่วนลด: {pay:,.2f} บาท")
        except ValueError:
            print("กรุณากรอกยอดซื้อเป็นตัวเลขเท่านั้น")
    elif eligible == "No":
        print(f"\n คุณยังไม่สามารถเข้าร่วมแคมเปญคนละครึ่งได้")
    else:
        print("\nเกิดข้อผิดพลาดของข้อมูลสิทธิ์ กรุณาติดต่อเจ้าหน้าที่")

    conn.close()

if __name__ == "__main__":
    init_db()   
    chatbot()
