import sqlite3

conn = sqlite3.connect('main_db.db')

cur = conn.cursor()

def main():
    with sqlite3.connect('main_db.db') as conn:
        cur = conn.cursor()
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS main_db (
                        id INTEGER PRIMARY KEY, 
                        device_serial_number TEXT, 
                        payment_status BOOLEAN, 
                        device_status BOOLEAN
                    )""")

def get_payment_status(device_serial_number):
    with sqlite3.connect('main_db.db') as conn:
        cur = conn.cursor()
        cur.execute("""
                    SELECT payment_status FROM main_db
                    WHERE device_serial_number=?
                    """, (device_serial_number,))
        result = cur.fetchone()
        return result[0] if result else None
    
def get_device_status(device_serial_number):
    with sqlite3.connect('main_db.db') as conn:
        cur = conn.cursor()
        cur.execute("""
                    SELECT device_status FROM main_db
                    WHERE device_serial_number=?
                    """, (device_serial_number,))
        result = cur.fetchone()
        return result[0] if result else None    
    
def update_payment(device_serial_number, paid):
    with sqlite3.connect('main_db.db') as conn:
        cur = conn.cursor()
        cur.execute("""
                    UPDATE main_db
                    SET payment_status = ?
                    WHERE device_serial_number = ?
                    """, (paid, device_serial_number))
        return {'status': 'success'}
    
def update_onoff(device_serial_number, onoff):
    with sqlite3.connect('main_db.db') as conn:
        cur = conn.cursor()
        cur.execute("""
                    UPDATE main_db
                    SET device_status = ?
                    WHERE device_serial_number = ?
                    """, (onoff, device_serial_number))
        return {'status': 'success'}
        
def write_data():
    with sqlite3.connect('main_db.db') as conn:
        cur = conn.cursor()
        cur.execute("""
                    INSERT INTO main_db (id, device_serial_number, payment_status, device_status)
                    VALUES (?, ?, ?, ?)
                    """, (1, "NTR987654312", 0, 0))

# print(get_payment_status('NTR987654312'))
# print(get_device_status('NTR987654312'))