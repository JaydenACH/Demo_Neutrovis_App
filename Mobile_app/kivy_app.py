from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.network.urlrequest import UrlRequest
from kivy.clock import Clock
from datetime import datetime
import requests
import urllib3
import json
import time


# address:str = 'http://localhost:8000'
address = 'https://demo_backend_api-2-z7709942.deta.app'
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# NTR987654312

class ScrollableTextInput(TextInput):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if touch.is_mouse_scrolling:
                return False
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos):
            if touch.is_mouse_scrolling:
                return False
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if touch.is_mouse_scrolling:
            return False
        return super().on_touch_up(touch)


class KivyApp(App):
    def build(self):
        self.layout_main = BoxLayout(orientation='vertical')
        
        # grid layouts as tables
        self.layout = GridLayout(cols=2)

        self.layout.add_widget(Label(text="Device Serial Number"))
        self.serialnumber = Label(text="NTR987654312")
        self.layout.add_widget(self.serialnumber)
        
        self.layout.add_widget(Label(text="Payment Status"))
        self.paystatus = Label(text="")
        self.layout.add_widget(self.paystatus)

        self.layout.add_widget(Label(text="Device Status"))
        self.devicestatus = Label(text="")
        self.layout.add_widget(self.devicestatus)

        self.pay_button_container = AnchorLayout(anchor_x='center', anchor_y='center')
        self.pay_button = Button(text="Pay", size_hint=(None, None), size=(100, 50), padding=(10, 10))
        self.pay_button_container.add_widget(self.pay_button)
        self.layout.add_widget(self.pay_button_container)
        self.pay_button.bind(on_release=lambda instance: self.payment(1))

        self.on_off_button_container = AnchorLayout(anchor_x='center', anchor_y='center')
        self.on_off_button = Button(text="On/Off", size_hint=(None, None), size=(100, 50), padding=(10, 10))
        self.on_off_button_container.add_widget(self.on_off_button)
        self.layout.add_widget(self.on_off_button_container)
        self.on_off_button.bind(on_release=self.power_onoff)
        
        # add grid layout into box layout
        self.layout_main.add_widget(self.layout)
        
        self.textinput = ScrollableTextInput(multiline=True, size_hint_y=1, padding=(10, 10))
        scrollview = ScrollView(size_hint=(1, 1), size=(self.layout.width, self.layout.height))
        scrollview.add_widget(self.textinput)
        self.layout_main.add_widget(scrollview)
        
        self.get_all_status(self.serialnumber) 
        return self.layout_main

        
    def get_all_status(self, instance):
        pay_response, dev_response = self.get_requests()
        
        if pay_response:
            self.paystatus.text = "Paid"
        else:
            self.paystatus.text = "Not Paid"
        
        if dev_response:
            self.devicestatus.text = "On"
        else:
            self.devicestatus.text = "Off"
        
        self.log_in_app('Starting app', pay_response, dev_response)
           
    def payment(self, paid: int):
        url = f"{address}/paynow/{paid}"
        headers = {"Content-Type": "application/json"}
                
        UrlRequest(url, method="PUT", req_headers=headers, verify=False)
        self.paystatus.text = "Paid" if paid == 1 else "Not pay yet"
        
        pay_response, dev_response = self.get_requests()
        self.log_in_app('Payment', paid, dev_response)
        
    def power_onoff(self, instance):
        pay_response, dev_response = self.get_requests()
        onoff = 0 if dev_response else 1
        address3 = address + f"/onoffdev/{onoff}"
        
        headers = {"Content-Type": "application/json"}
        data = {
            "device_serial_number": self.serialnumber.text,
            "onoff": onoff,
        }
                
        if pay_response:
            if dev_response:
                UrlRequest(address3, method="PUT", req_headers=headers, 
                           req_body=json.dumps(data), verify=False)
                self.devicestatus.text = "Off"
                self.log_in_app('Device status', pay_response, 0)
            else:
                UrlRequest(address3, method="PUT", req_headers=headers, 
                           req_body=json.dumps(data), verify=False)
                self.devicestatus.text = "On"
                self.log_in_app('Device status', pay_response, 1)
        elif dev_response:
            UrlRequest(address3, method="PUT", req_headers=headers, 
                       req_body=json.dumps(data), verify=False)
            self.devicestatus.text = "Off"
            self.log_in_app('Device status', pay_response, 0)
        else:
            self.devicestatus.text = "Cannot turn on until payment done"
            self.paystatus.text = "Expired"
            self.log_in_app('Device status', pay_response, 0)

    def curr_datetime(self):
        now = datetime.now()
        datetime_string = now.strftime("%Y-%m-%d %H:%M")
        return datetime_string

    def log_in_app(self, action:str, pay_response: int, dev_response: int):
        log = f"{self.curr_datetime()} - [{action}] Payment = {'Paid' if pay_response else 'Not paid'}; Device = {'On' if dev_response else 'Off'}"
        self.textinput.text += log + '\n' 
        
    def get_requests(self):
        address1 = f"{address}/getpaymentstatus"
        address2 = f"{address}/getdevicestatus"
        try:
            pay_response = requests.get(address1, verify=False).json()['data']
            dev_response = requests.get(address2, verify=False).json()['data']
            return [pay_response, dev_response]
        except requests.exceptions.HTTPError as errh:
            self.log_in_app('HTTPError', 0, 0)
            self.disable_buttons()
            return [0, 0]
        except requests.exceptions.ConnectionError as errc:
            self.log_in_app('ConnectionError', 0, 0)
            self.disable_buttons()
            return [0, 0]
    
    def display_error(self, title, message):
        content = Label(text=message)
        popup = Popup(title=title, content=content, size_hint=(0.5, 0.5))
        popup.open()
        
    def disable_buttons(self):
        self.pay_button.disabled = True
        self.on_off_button.disabled = True
        
    
if __name__ == "__main__":
    KivyApp().run()
