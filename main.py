from fastapi import FastAPI
from query_db import get_payment_status, get_device_status, update_payment, update_onoff
from deta_base import create, read, update, delete

app = FastAPI()

@app.get("/")
def main():
    return {"data": "All is working"}

@app.get('/getpaymentstatus')
def getpaymentstatus():
    result = read()
    status = result['payment_status']
    return {'data': 1 if status else 0}

@app.get('/getdevicestatus')
def getdevicestatus():
    result = read()
    status = result['device_status']
    return {'data': 1 if status else 0}

@app.put('/paynow/{paid}')
def paynow(paid: int):
    return update('payment_status', paid)

@app.put('/onoffdev/{onoff}')
def onoffdev(onoff: int):
    return update('device_status', onoff)

deta_token = 'oshdshSW_iUFNJZq8zEkzqTsxanrmiknoFYm2aghu'