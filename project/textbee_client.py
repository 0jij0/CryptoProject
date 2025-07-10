import requests

class TextBeeClient:
    def __init__(self, api_key, device_id):
        self.api_key = api_key
        self.device_id = device_id
        self.base_url = "https://api.textbee.dev/api/v1"

    def send_sms(self, phone_number, message):
        url = f"{self.base_url}/gateway/devices/{self.device_id}/send-sms"
        payload = {
            "recipients": [phone_number],
            "message": message
        }
        
        headers = {"x-api-key": self.api_key}
        response = requests.post(url, json=payload, headers=headers)
        return response.json()

    def fetch_incoming_sms(self):
        url = f"{self.base_url}/gateway/devices/{self.device_id}/get-received-sms"
        headers = {"x-api-key": self.api_key}
        resp = requests.get(url, headers=headers)
        return resp.json()
