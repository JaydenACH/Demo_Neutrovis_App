from deta import Deta

data_key = 'a0YuU7iNwQBV_TP2rz2J6XZQCEKWiC3mzkVxkVjSWXPEd'
deta = Deta(data_key)

db = deta.Base("deta_db")

data = {
    'device_serial_number': 'NTR987654312',
    'payment_status': False,
    'device_status': False
}

def create(data):
    result = db.put(data)
    return result

def read(data=''):
    # return a dictionary same as data above
    records = db.fetch()
    return records.items[0]

def update(key, status: bool):
    record = read()
    if key in record:
        record[key] = status
        db.put(record)
        return {'status': 'success'}
    return {'status': 'fail'}

def delete():
    records = db.fetch()
    for record in records.items:
        for rec in record:
            db.delete(record['key'])

# delete()
# create(data)
