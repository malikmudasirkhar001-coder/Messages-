import time
import requests
import json
import os

# FIREBASE DATABASE URL
FIREBASE_URL = "https://mysmsbridge-8f994-default-rtdb.firebaseio.com/sms_messages.json"

processed_keys = set()

def send_android_notification(title, message):
    """
    Termux / Android System Native Notification Trigger
    """
    # 1. Termux Notification Support
    os.system(f'termux-notification --title "{title}" --content "{message}" --vibrate 300,150,300 --sound')
    
    # 2. Print Log for Pydroid / Python Console
    print(f"==========================================")
    print(f"[SYSTEM NOTIFICATION SENT]")
    print(f"Title: {title}")
    print(f"Message: {message}")
    print(f"==========================================")

def listen_firebase_messages():
    global processed_keys
    print("Connecting to Firebase SMS Notification Bridge...")
    
    # Initial load to fetch existing keys so we don't notify for old messages
    try:
        response = requests.get(FIREBASE_URL)
        if response.status_code == 200 and response.json():
            data = response.json()
            for key in data.keys():
                processed_keys.add(key)
        print("Initial synchronization complete. Listening for NEW incoming SMS...")
    except Exception as e:
        print(f"Connection Error: {e}")

    while True:
        try:
            response = requests.get(FIREBASE_URL)
            if response.status_code == 200 and response.json():
                data = response.json()
                for key, val in data.items():
                    if key not in processed_keys:
                        sender = val.get('sender', 'New SMS')
                        msg_text = val.get('msg', '')
                        
                        # Trigger system notification
                        send_android_notification(f"New Message from {sender}", msg_text)
                        processed_keys.add(key)
        except Exception as e:
            pass
            
        time.sleep(2)  # Check every 2 seconds

if __name__ == "__main__":
    listen_firebase_messages()
