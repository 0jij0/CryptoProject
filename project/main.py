import random
import time
from encryptor import encrypt, decrypt
from textbee_client import TextBeeClient

# --- CONFIG ---
API_KEY = "e6332433-57f0-4080-a325-b7a665bf0933"
DEVICE_ID = "6861a02c271d07458070e170"
PHONE_NUMBER = "+254707694756"

# --- Initialize client ---
tb = TextBeeClient(API_KEY, DEVICE_ID)

# --- Generate OTP + Encrypt message ---
otp = ''.join([str(random.randint(0, 9)) for _ in range(16)])
message = input("Enter the message to encrypt: ")
encrypted_msg = encrypt(message, otp)

print("\nEncrypted Message:\n", encrypted_msg)

# --- Send SMS via TextBee.dev ---
sms_body = f"Your OTP for AES message is: {otp}\nPlease reply EXACTLY with this OTP."
sms_resp = tb.send_sms(PHONE_NUMBER, sms_body)
print("\nTextBee API Response:\n", sms_resp)

# --- Wait and fetch incoming SMS ---
print("\nWaiting 30 seconds for reply...")
time.sleep(30)

incoming = tb.fetch_incoming_sms()
sms_data = incoming.get("data", [])

if sms_data:
    sms_text = sms_data[0]["message"]
    sender = sms_data[0]["sender"]
    print(f"\nIncoming SMS from {sender}: {sms_text}")

    # Extract OTP from reply (assumes last word is OTP)
    otp_from_sms = sms_text.strip().split()[-1]

    # Check OTP length
    if len(otp_from_sms) != 16:
        print(f"\nInvalid OTP length: {len(otp_from_sms)}. Expected 16 digits.")
    else:
        try:
            decrypted_msg = decrypt(encrypted_msg, otp_from_sms)
            print("\n✅ Decrypted Message:\n", decrypted_msg)
        except Exception as e:
            print("Failed to decrypt:", e)
else:
    print("No incoming SMS found.")
