from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from encryptor import encrypt, decrypt
from textbee_client import TextBeeClient
import random
import os
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for flashing messages

API_KEY = os.getenv("API_KEY")
DEVICE_ID = os.getenv("DEVICE_ID")
PHONE_NUMBER = "+254707694756"
tb = TextBeeClient(API_KEY, DEVICE_ID)

@app.route('/')
def index():
    # Add usage instructions and example data for the user
    instructions = (
        "1. Enter your message and click 'Encrypt & Send OTP'.<br>"
        "2. The OTP will be sent to your phone.<br>"
        "3. Use the OTP to decrypt the message below.<br>"
        "4. You can copy the encrypted message and OTP for later use."
    )
    example_message = "Hello, this is a secret!"
    return render_template('index.html', instructions=instructions, example_message=example_message)

@app.route('/send', methods=['POST'])
def send():
    message = request.form['message']
    phone_number = request.form['phone_number']
    if not message.strip():
        return jsonify({'error': 'Message cannot be empty.'}), 400
    if not phone_number.strip():
        return jsonify({'error': 'Phone number cannot be empty.'}), 400
    otp = ''.join([str(random.randint(0, 9)) for _ in range(16)])
    encrypted_msg = encrypt(message, otp)
    sms_body = f"Your OTP for AES message is: {otp}\nPlease reply EXACTLY with this OTP."
    tb.send_sms(phone_number, sms_body)
    return jsonify({
        'encrypted': encrypted_msg,
        'info': 'OTP sent to your phone. Use it to decrypt the message below.'
    })

@app.route('/decrypt', methods=['POST'])
def decrypt_msg():
    encrypted_msg = request.form['encrypted']
    otp = request.form['otp']
    if not encrypted_msg.strip() or not otp.strip():
        return jsonify({'error': 'Both Encrypted message and OTP are required.'}), 400
    try:
        decrypted = decrypt(encrypted_msg, otp)
        return jsonify({'decrypted': decrypted})
    except Exception as e:
        return jsonify({'error': 'Failed to decrypt. Please check your OTP and encrypted message.'}), 400

if __name__ == '__main__':
    app.run(debug=True)
