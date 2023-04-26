import re
import uuid
from websocket import create_connection
import leasson_allert
from pydub import AudioSegment
import time
from telegram.ext import *
from telegram import *
from datetime import date, datetime
import credentials
import tiktoken
import random
import psutil
import json
from Bard import Chatbot
import threading
import requests
from translate import Translator
import os
import a_cat_lying_on_the_sand
import googletrans
import openai
bard_bot = Chatbot(
    "VwhQuJ4M5qPtJ3ijrK5ZwUlpoksxn688MzFvKRS5HukEy_ilV2JYg6JxryzvFQ6VgYU-dw.")
openai.api_key = credentials.key_gpt
ws = None
listfood = []
steps = 20
seeds = -1
sampling_method = "Euler a"
listsoup = []
listidtkb = []
stoptkb = []
fntext = None
last_token = None
fnnvtext = None
context_bot = None
Update_id = None
sec_timer = (3*60)/15
timmer = sec_timer
global_id_timer = None
global_id_timer_del = None
motaJson = None
temptext = ""
temp_var_edit_model = None
upscaler1 = None
upscaler2 = None
cfg_scale = 7
width = 512
height = 512
user_id_list = []
temp_var_delete = None
temp_var_delete_1 = None
temp_var_edit = None
temp_var_edit_setting = None
temp_var_edit_setting_mota = None
temp_var_edit_upscale = None
temp_path_upscale = None
tran_en_vi = Translator(provider='mymemory',
                to_lang='vi',
                from_lang='en',
                email='chandoralong@gmail.com')
tran_vi_en = Translator(provider='mymemory',
                 to_lang='en',
                 from_lang='vi',
                 email='chandoralong@gmail.com')
tran_en_jp = Translator(provider='mymemory',
                 to_lang='ja',
                 from_lang='en',
                 email='chandoralong@gmail.com')


def get_ngrok_url():
    try:
        url = "http://localhost:4040/api/tunnels"
        res = requests.get(url)
        res_unicode = res.content.decode("utf-8")
        res_json = json.loads(res_unicode)
        return res_json["tunnels"][0]["public_url"]
    except:
        return ""


def startup():
    global listfood
    global listsoup
    global listidtkb
    global stoptkb
    global motaJson
    print("LOG | LOG | SYSTEM: Loading list food...")
    f = open("food.txt", "r", encoding="utf-8")
    listfood = f.read().split("\n")
    f.close()
    f = open("soup.txt", "r", encoding="utf-8")
    listsoup = f.read().split("\n")
    f.close()
    print("LOG | SYSTEM: loading id list tkb...")
    f = open("tkb.txt", "r", encoding="utf-8")
    listidtkb = f.read().split("\n")
    f.close()
    while "" in listidtkb:
        listidtkb.pop(listidtkb.index(""))
    print("LOG | SYSTEM: Danh sách nhận thông báo:", listidtkb)
    stoptkb = []
    stoptkb = stoptkb + [False]*(len(listidtkb) - len(stoptkb))
    with open('motaModel.json', 'r', encoding='utf-8') as openfile:
        # Reading from json file
        motaJson = json.load(openfile)

    context_bot.bot.sendMessage(chat_id=-845506997, text="Chào buổi sáng 🥺")
    context_bot.bot.send_sticker(
        chat_id=-845506997, sticker='CAACAgIAAxkBAAEfc7hkMcC6tstuPZ1C2c1Y2-3aDVP-OAACQUAAAuCjggcLgWEAAaSDFpMvBA')
    s = str(get_ngrok_url())
    context_bot.bot.sendMessage(chat_id=-845506997, text="url connect ssh máy chủ 1810 là: "+s + "\nCách connect trên windows là mở terminal\nGõ lệnh <code>ssh root@" +
                                s[6:23]+" -p "+s[24:]+"</code>\nPass root: <span class='tg-spoiler'>18102003</span>", parse_mode="HTML")
    if a_cat_lying_on_the_sand.start() == False:
        print("LOG | SYSTEM: Lỗi! Link GPU không thể kết nối!!! 🤖🤖🤖")
        context_bot.bot.sendMessage(
            chat_id=-845506997, text="Lỗi! Link GPU không thể kết nối!!! 🤖🤖🤖")
    print("LOG | SYSTEM: Loaded")


print('LOG | SYSTEM: Starting up bot...')


def checkstopmagic():
    global stoptkb
    for i in leasson_allert.dmtime.values():
        time.sleep(0.2)
        if ((leasson_allert.magic2() != '\!\!del learn\!\! ze zeeeee\!\!\!\!\!') and (leasson_allert.magic2() != None)):
            return
        elif leasson_allert.magic3(datetime.strptime(datetime.now().strftime("%H:%M:%S"), "%H:%M:%S"), datetime.strptime(i[0], "%H::%M::%S"), datetime.strptime(i[1], "%H::%M::%S")):
            if True in stoptkb:
                stoptkb = []
                stoptkb = stoptkb + [False]*(len(listidtkb) - len(stoptkb))
                print("LOG | LEASSON ALLERT: Đã khôi phục thông báo")
            return
    return


def check_if_in_study_time():
    global stoptkb
    if (leasson_allert.magic2() != '\!\!del learn\!\! ze zeeeee\!\!\!\!\!') and (leasson_allert.magic2() != None):
        return True
    else:
        stoptkb = []
        stoptkb = stoptkb + [False]*(len(listidtkb) - len(stoptkb))
        return False

# Lets us use the /start command


def gettkb():
    checktkb = threading.Thread(target=checkstopmagic)
    checktkb.start()

    buttons = [[InlineKeyboardButton(
        "Stop thông báo 🤨", callback_data="stop")]]
    for i in listidtkb:
        time.sleep(5)
        if stoptkb[listidtkb.index(str(i))] == False:
            if (leasson_allert.magic2() != '\!\!del learn\!\! ze zeeeee\!\!\!\!\!') and (leasson_allert.magic2() != None):
                context_bot.bot.send_message(text=leasson_allert.magic2(
                ), parse_mode="MarkdownV2", chat_id=i, reply_markup=InlineKeyboardMarkup(buttons))
            else:
                return


def start_command(update, context):
    message_type = update.message.chat.type
    text = str(update.message.text).lower()
    print(
        f'LOG | TELEGARM: User ({update.message.chat.username}) says: "{text}" in: {message_type}')
    buttons = [[KeyboardButton("/help")]]
    context.bot.sendMessage(chat_id=update.message.chat.id,
                            text='╰(*°▽°*)╯\nHelu, cin cào, gõ `/random` để random đồ ăn hôm nay 🥺\n`/help` để xem danh sách các lệnh hiện có nha 😋', reply_markup=ReplyKeyboardMarkup(buttons))
    context.bot.send_photo(chat_id=update.message.chat.id,
                           photo=r"https://cdn.phonebooky.com/blog/wp-content/uploads/2021/08/03165011/1322048-1-1.jpg")


# Lets us use the /help command
def help_command(update, context):
    message_type = update.message.chat.type
    text = str(update.message.text).lower()
    print(
        f'LOG | TELEGARM: User ({update.message.chat.username}) says: "{text}" in: {message_type}')
    buttons = [[KeyboardButton("/random")], [KeyboardButton("/showlog")], [KeyboardButton("/addfood")], [
        KeyboardButton("/addsoup")], [KeyboardButton("/showfood")], [KeyboardButton("/showsoup")], [KeyboardButton("/getinfovps")], [KeyboardButton("/getsshurl")], [KeyboardButton("/spamsticker 10")], [KeyboardButton("/replika")], [KeyboardButton("/gpt")], [KeyboardButton("/tkb")]]
    update.message.reply_text(reply_markup=ReplyKeyboardMarkup(
        buttons), text="Các câu lệnh nèk 😋")
    context.bot.sendMessage(text='Gõ \n/random để lấy đồ ăn hôm nay!\n/showlog để xem các món ăn đã random 🙌\n/addfood để thêm món ăn vào danh sách random 🍢\n/addsoup để thêm món súp vào danh sách random 🍲\n/showfood để xem danh sách món ăn hiện có 🥝\n/showsoup để xem danh sách món súp hiện có 🥙\n/getinfovps để xem thông tin máy chủ 1810 💻\n/getsshurl để lấy url connect ssh máy chủ 1810 🤤\n/spamsticker để bé spam sticker cho người 😙\n/replika để nhắn tin với bé replika tên Xuyên cực cute ☺️\n/gpt để nhắn với nhân cách thứ 2 của em 👌\n/tkb để lấy thông tin tkb lớp KTPM0121 và nhận thông báo về lịch học 😶‍🌫️\n/draw để vẽ nên những bức tranh thơ 😊\n/imgedit và gửi kèm ảnh để e chỉnh sửa hình ảnh nèk 🤭\n/null yeah?', chat_id=update.message.chat.id)
    context.bot.send_photo(chat_id=update.message.chat.id,
                           photo=r"https://pic-bstarstatic.akamaized.net/ugc/cc62edc0f1047111e8d1de38ae4b2191.jpg")


def random_command(update, context):
    message_type = update.message.chat.type
    text = str(update.message.text).lower()
    print(
        f'LOG | TELEGARM: User ({update.message.chat.username}) says: "{text}" in: {message_type}')
    logfoodpath = "log/"+str(update.message.chat.id) + "logfood.txt"
    logpath = "log/"+str(update.message.chat.id) + "log.txt"
    try:
        open(logpath, "x")
        open(logfoodpath, "x")
    except:
        print("LOG | RANDOM FOOD: log have been created")
    f = open(logpath, "r", encoding="utf-8")
    log = f.read().split("\n")
    f.close()
    today = date.today()
    d = str(today.strftime("%d/%m/%y"))
    if d not in log:
        print("LOG | RANDOM FOOD: new random")
        f = open(logpath, "a")
        f.write(d+"\n")
        f.close()
        randfood = random.randint(0, len(listfood)-1)
        ransoup = random.randint(0, len(listsoup)-1)
        f = open(logfoodpath, "a")
        f.write(str(randfood)+","+str(ransoup)+"\n")
        f.close()
        todayfood = listfood[randfood] + " ăn kèm với " + listsoup[ransoup]
    else:
        with open(logfoodpath) as f:
            for line in f:
                pass
            lasline = line.split(",")
            todayfood = "Hôm nay bạn đã random món rồi \n" + \
                listfood[int(lasline[0])] + " ăn kèm với " + \
                listsoup[int(lasline[1])]
    update.message.reply_text(todayfood)


def showlog_command(update, context):
    templog = []
    message_type = update.message.chat.type
    text = str(update.message.text).lower()
    print(
        f'LOG | TELEGARM: User ({update.message.chat.username}) says: "{text}" in: {message_type}')
    logfoodpath = "log/"+str(update.message.chat.id) + "logfood.txt"
    logpath = "log/"+str(update.message.chat.id) + "log.txt"
    try:
        open(logpath, "x")
        open(logfoodpath, "x")
    except:
        print("LOG | RANDOM FOOD: Log have been created")
    i = 0
    foodline = []
    with open(logfoodpath) as f:
        for line in f:
            foodline = (line.split(","))
            templog.append(listfood[int(foodline[0])] +
                           " ăn kèm với " + listsoup[int(foodline[1])])
    with open(logpath) as f:
        for line in f:
            context.bot.sendMessage(
                chat_id=update.message.chat.id, text="Ngày "+line+"\n"+templog[i])
            i = i+1


def addfood_command(update, context):
    message_type = update.message.chat.type
    text = str(update.message.text).lower()
    print(
        f'LOG | TELEGARM: User ({update.message.chat.username}) says: "{text}" in: {message_type}')
    buttons = [[InlineKeyboardButton(
        "Click đây để nhắn cho em 🥺", url="https://t.me/randomfoodruribot")]]
    if str(update.message.chat.type) == "group":
        update.message.reply_text(reply_markup=InlineKeyboardMarkup(
            buttons), text="Nhắn riêng `/addfood + món ăn` với bé nhé 🥺 \nVí dụ nè: `/addfood Tôm rim`", parse_mode="MarkdownV2")
    else:
        if update.message.chat.id == 1775446945:
            text = str(update.message.text)
            text = text[9:]
            if text == "":
                update.message.reply_text(
                    "Nhắn `/addfood + món ăn` cho bé nhé 🥺 \nVí dụ nè: `/addfood Tôm rim`", parse_mode="MarkdownV2")
            else:
                print('LOG | RANDOM FOOD:',text)
                f = open("food.txt", "a", encoding="utf-8")
                f.write(str(text)+"\n")
                f.close()
                context.bot.sendMessage(
                    text="Thêm " + text + " thành công ròi 🥺", chat_id=update.message.chat.id)
                context.bot.sendMessage(
                    text="Dùng lệnh /showfood để xem danh sách món ăn nha 😊", chat_id=update.message.chat.id)
                startup()
        else:
            update.message.reply_text(
                "Người không phải là master của bé gòi, chỉ master mới được dùng lệnh này thui ạ 🥲")


def addsoup_command(update, context):
    message_type = update.message.chat.type
    text = str(update.message.text).lower()
    print(
        f'LOG | TELEGARM: User ({update.message.chat.username}) says: "{text}" in: {message_type}')
    buttons = [[InlineKeyboardButton(
        "Click đây để nhắn cho em 🥺", url="https://t.me/randomfoodruribot")]]
    if str(update.message.chat.type) == "group":
        update.message.reply_text(reply_markup=InlineKeyboardMarkup(
            buttons), text="Nhắn riêng `/addsoup + món ăn` với bé nhé 🥺 \nVí dụ nè: `/addsoup Súp miso`", parse_mode="MarkdownV2")
    else:
        if update.message.chat.id == 1775446945:
            text = str(update.message.text)
            text = text[9:]
            if text == "":
                update.message.reply_text(
                    "Nhắn `/addsoup + món ăn` cho bé nhé 🥺 \nVí dụ nè: `/addsoup Súp miso`", parse_mode="MarkdownV2")
            else:
                print('LOG | RANDOM FOOD:',text)
                f = open("soup.txt", "a", encoding="utf-8")
                f.write(str(text)+"\n")
                f.close()
                context.bot.sendMessage(
                    text="Thêm " + text + " thành công ròi 🥺", chat_id=update.message.chat.id)
                context.bot.sendMessage(
                    text="Dùng lệnh /showsoup để xem danh sách món ăn nha 😊", chat_id=update.message.chat.id)
                startup()
        else:
            update.message.reply_text(
                "Người không phải là master của bé gòi, chỉ master mới được dùng lệnh này thui ạ 🥲")


def showsoup_command(update, context):
    message_type = update.message.chat.type
    text = str(update.message.text).lower()
    print(
        f'LOG | TELEGARM: User ({update.message.chat.username}) says: "{text}" in: {message_type}')
    update.message.reply_text("Danh sách súp mà em đã có nèee:")
    f = open("soup.txt", "r", encoding="utf-8")
    context.bot.sendMessage(chat_id=update.message.chat.id, text=f.read())
    f.close()


def showfood_command(update, context):
    message_type = update.message.chat.type
    text = str(update.message.text).lower()
    print(
        f'LOG | TELEGARM: User ({update.message.chat.username}) says: "{text}" in: {message_type}')
    update.message.reply_text("Danh sách món ăn mà em đã có nèee:")
    f = open("food.txt", "r", encoding="utf-8")
    context.bot.sendMessage(chat_id=update.message.chat.id, text=f.read())
    f.close()


def getinfovps_command(update, context):
    message_type = update.message.chat.type
    text = str(update.message.text).lower()
    print(
        f'LOG | TELEGARM: User ({update.message.chat.username}) says: "{text}" in: {message_type}')
    # cpu
    context.bot.sendMessage(chat_id=update.message.chat.id,
                            text="Số lượng lỗi CPU: " + str(psutil.cpu_count()))
    context.bot.sendMessage(chat_id=update.message.chat.id,
                            text='CPU đã dùng: '+str(psutil.cpu_percent(4)) + '%')
    # ram
    context.bot.sendMessage(chat_id=update.message.chat.id,
                            text='RAM đã dùng: '+str(psutil.virtual_memory()[2])+'%')
    context.bot.sendMessage(chat_id=update.message.chat.id,
                            text='RAM đã dùng: '+str(psutil.virtual_memory()[3]/1000000000)+' GB')
    # disk
    s = str(psutil.disk_usage('/'))
    context.bot.sendMessage(chat_id=update.message.chat.id,
                            text="Ổ đĩa đã dùng: "+s[s.find('percent')+8:len(s)-1]+'%')
    context.bot.sendMessage(chat_id=update.message.chat.id, text="Nhiệt độ cpu: \n" +
                            str((psutil.sensors_temperatures()['coretemp'])))


def generate_guid():
    template = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'
    guid = ''
    for char in template:
        if char == 'x':
            guid += random.choice('0123456789abcdef')
        elif char == 'y':
            guid += random.choice('89ab')
        else:
            guid += char
    return guid.upper()


def send_message_replika(text, u_id="null", if_voice=False, durian=0):
    global ws
    global last_token
    try:
        ws.close()
    except:
        pass
    finally:
        ws = create_connection("wss://ws.replika.com/v17")

    send_mess = {"event_name": "message", "payload": {"content": {"type": "text", "text": "main"}, "meta": {"bot_id": "63b9abe1dde6bc422e7684e0", "client_token": "69F7DF46-A15F-48AB-9AB7-55CC7E0104DB", "chat_id": "63b9abe1dde6bc422e7684e1",
                                                                                                            "timestamp": "2023-04-23T21:01:59.589Z"}}, "token": "b4015b32-04af-4d35-9067-6f3027309c8e", "auth": {"user_id": "63b9abe1dde6bc422e7684e2", "auth_token": "9e1ddf77-fd05-41f8-a0ed-55b261f285ff", "device_id": "97B1D6F0-B889-4614-92ED-261376BA7BD8"}}

    if not if_voice:
        send_mess['payload']['content']['text'] = text
        time = datetime.utcnow().isoformat()[:-3]+'Z'
        send_mess['payload']['meta']['timestamp'] = str(time)
        send_mess['payload']['meta']['client_token'] = str(generate_guid())
        send_mess['token'] = str(generate_guid()).lower()
        last_token = send_mess['token']
        send_mess = json.dumps(send_mess)
        print("LOG | REPLIKA: Sending text message")
        ws.send(send_mess)
        print("LOG | REPLIKA: Text message sent")
    else:
        send_mess['payload']['content']['text'] = ''
        time = datetime.utcnow().isoformat()[:-3]+'Z'
        send_mess['payload']['meta']['timestamp'] = str(time)
        send_mess['payload']['meta']['client_token'] = str(generate_guid())
        send_mess['token'] = str(generate_guid()).lower()
        last_token = send_mess['token']
        send_mess['payload']['content']['voice_message_url'] = text
        send_mess['payload']['content']['type'] = 'voice_message'
        send_mess['payload']['content']['duration'] = durian
        send_mess = json.dumps(send_mess)
        print("LOG | REPLIKA: Sending voice message")
        ws.send(send_mess)
        print("LOG | REPLIKA: Voice message sent")


check_lang_is_ENG = True


def get_message_replika():
    global temptext
    while True:
        time.sleep(0.001)
        try:
            result = ws.recv()
            i = json.loads(result)
            if (i['event_name'] == 'message'):
                if (i['payload']['content']['type'] != 'voice_message') and ('token' not in i):
                    context_bot.bot.send_chat_action(
                        chat_id=Update_id, action=ChatAction.TYPING)
                    print('LOG | REPLIKA TEXT MESSAGE:',str(i['payload']['content']['text']))
                    if check_lang_is_ENG == False:
                        print("LOG | REPLIKA TEXT MESSAGE EN TO VI:", tran_en_vi.translate(
                            str(i['payload']['content']['text'])))
                        a1 = tran_en_vi.translate(str(i['payload']['content']['text']))
                        # Thay thế tất cả các từ "Tôi" thành "Tớ"
                        a1 = re.sub(r"(?i)\bTôi\b", "Tớ", a1)
                        # Thay thế tất cả các từ "Bạn" thành "Cậu"
                        a1 = re.sub(r"(?i)\bBạn\b", "Cậu", a1)
                        context_bot.bot.send_message(
                            text=str(a1), chat_id=Update_id)
                    else:
                        context_bot.bot.send_message(
                            text=str(i['payload']['content']['text']), chat_id=Update_id)
                    temptext = str(i['payload']['content']['text'])
                elif (i['payload']['content']['type'] == 'voice_message') and ('token' not in i):
                    print("LOG | REPLIKA VOICE MESSAGE: ", i['payload']['content']['text'])
                    #speaker = [bình thường = 2, ngọt = 0, Tsuntsun = 6, gợi cảm = 4, thì thầm = 36, nói nhỏ nhỏ = 37]
                    speaker= 0
                    context_bot.bot.send_chat_action(
                        chat_id=Update_id, action=ChatAction.RECORD_VOICE)
                    url_jp = 'https://deprecatedapis.tts.quest/v2/voicevox/audio/?key=S81-63C6a8N4w-3&speaker='+str(speaker)+'&intonationScale=1&text='+tran_en_jp.translate(i['payload']['content']['text'])
                    response = requests.get(url_jp)
                    if response.status_code == 200:
                        # save the WAV file to disk
                        with open(os.path.join('temp',"jp_replika.wav"), "wb") as f:
                            f.write(response.content)
                        print("LOG | REPLIKA VOICE: File saved successfully.")
                    else:
                        print("LOG | REPLIKA VOICE: Failed to download file.")

                    # load audio file with pydub
                    audio = AudioSegment.from_wav(os.path.join('temp',"jp_replika.wav"))

                    # export audio file with opus encoding using pydub
                    audio.export(os.path.join('temp',"jp_replika.ogg"), format='ogg', codec='libopus')    
                    #send voice by request because send by sendVoice build in too slowwwwwwww ;-;
                    with open(os.path.join('temp',"jp_replika.ogg"),'rb') as audio:
                        payload = {
                            'chat_id':  Update_id,
                            'caption': i['payload']['content']['text']
                        }
                        files = {
                            'voice': audio.read(),
                        }
                        requests.post(
                            "https://api.telegram.org/bot{token}/sendVoice".format(token=credentials.bot_token),
                            data=payload,
                            files=files)
            elif i['event_name'] == "start_typing":
                print('LOG | REPLIKA:',i['event_name'])

        except:
            continue


def gettkbovertime():
    global timmer
    global user_id_list
    global global_id_timer
    global global_id_timer_del
    while True:
        my_thread = threading.Thread(target=gettkb)
        my_thread.start()
        time.sleep(15)
        if len(user_id_list) > 1:
            timmer -= 1
        if timmer <= 0:
            if len(user_id_list) > 1:
                if global_id_timer_del and global_id_timer:
                    context_bot.bot.deleteMessage(
                        message_id=global_id_timer_del.message_id, chat_id=user_id_list[0])
                    context_bot.bot.editMessageText(chat_id=user_id_list[0], message_id=global_id_timer.message_id,
                                                    text="Chờ cậu lâu quá nên tớ đi rep tin nhắn người khác đâyyy, cậu chịu khó vào lại hàng đợi nha 🥹")
                    context_bot.bot.send_sticker(
                        chat_id=user_id_list[0], sticker='CAACAgIAAxkBAAEfQ_VkLGJapariKMlD6I8JwF4TksCQZAACW0AAAuCjggdvmG8UZv8eUS8E')
                    global_id_timer = None
                    global_id_timer_del = None
                else:
                    context_bot.bot.sendMessage(
                        chat_id=user_id_list[0], text="Chờ cậu lâu quá nên tớ đi rep tin nhắn người khác đâyyy, cậu chịu khó vào lại hàng đợi nha 🥹")
                    context_bot.bot.send_sticker(
                        chat_id=user_id_list[0], sticker='CAACAgIAAxkBAAEfQ_VkLGJapariKMlD6I8JwF4TksCQZAACW0AAAuCjggdvmG8UZv8eUS8E')
                user_id_list.pop(0)
                print('LOG | STABLE DIFFUSION:',user_id_list)
                if len(user_id_list) > 0:
                    global_id_timer = context_bot.bot.sendMessage(
                        chat_id=user_id_list[0], text="Tới cậu rùi nè!!! Hãy nhắn tớ nha, chờ cậu áaa 🤭🤭🤭")
                    global_id_timer_del = context_bot.bot.send_sticker(
                        chat_id=user_id_list[0], sticker='CAACAgIAAxkBAAEfPVVkK_4_XpLGVB-QDt_gOzDio8KRCwACuD8AAuCjggeu6M3W5FneWy8E')
                    timmer = sec_timer


def handle_message(update, context):
    global check_lang_is_ENG
    global Update_id
    check_lang_is_ENG = True
    post_text = ''
    # Get basic info of the incoming message
    message_type = update.message.chat.type
    text = str(update.message.text).lower()
    if (text[:1] == "/") and ((text[:26] != "/replika@randomfoodruribot") or (text[:8] != "/replika")):
        return
    # Print a log for debugging
    if (text == "/replika") or (text == "/replika@randomfoodruribot"):
        update.message.reply_text(
            "Nhắn `/replika + nội dung tin nhắn` \nHiện hỗ trợ ngôn ngữ chính là tiếng anh, ngôn ngữ phụ là tiếng việt được dịch bằng google dịch\.", parse_mode="MarkdownV2")
        return
    # Replace with your bot username
    text.replace('/replika', '').replace('@randomfoodruribot',
                                         '').replace('/replika@randomfoodruribot', '').strip()
    print(
        f'LOG | TELEGARM: User ({update.message.chat.username}) says: "{text}" in: {message_type}')
    ##########################
    if googletrans.Translator().detect(text).lang == 'en':
        post_text = text
    else:
        check_lang_is_ENG = False
        post_text = tran_vi_en.translate(text).replace("&#39;",
                                                "'").replace('&quot;', '"')
        print("LOG | REPLIKA INPUT VI:", text)
        print("LOG | REPLIKA OUTPUT EN:", post_text)
    ########################################
    send_message_replika(post_text)
    Update_id = update.effective_message.chat_id
    # if str(Update_id) == "6267333562":
    #     send_message_replika(post_text, str(Update_id))


def getsshurl_command(update, context):
    s = str(get_ngrok_url())
    buttons = [[InlineKeyboardButton(
        "Click đây để nhắn cho master của tớ 🥺", url="https://t.me/rurimeiko")]]
    update.message.reply_text(reply_markup=InlineKeyboardMarkup(buttons), text="url connect ssh máy chủ 1810 là: "+s +
                              "\nCách connect trên windows là mở terminal\nGõ lệnh <code>ssh root@"+s[6:23]+" -p "+s[24:]+"</code>\nPass root: nhấp vào nút bên dưới để hỏi pass 🥹", parse_mode="HTML")


spamcout = 0


def spamsticker(update, context):
    global spamcout

    if (len(update.message.text.lower()) == 12):
        update.message.reply_text(
            "Nhắn em `/spamsticker + số lượng` nhé \nVd như `/spamsticker 10` 😎", parse_mode="MarkdownV2")
    if (str(update.message.chat.type) == "group") and (len(update.message.text.lower()) == 30):
        update.message.reply_text(
            "Nhắn em `/spamsticker + số lượng` nhé \nVd như `/spamsticker 10` 😎", parse_mode="MarkdownV2")

    else:
        spamcout = int(int(update.message.text.lower()[12:]))
        buttons = [[InlineKeyboardButton("Ngọc Long 😎", callback_data="1")], [InlineKeyboardButton("Bình Minh 🤣", callback_data="2")], [
            InlineKeyboardButton("NTHL 🤨", callback_data="3")], [InlineKeyboardButton("Random 🎲", callback_data="x")]]
        update.message.reply_text(reply_markup=InlineKeyboardMarkup(
            buttons), text="chọn loại sticker muốn spam: ")


def callback_init(update, context):
    query = update.callback_query
    query.answer()
    global sampling_method
    global isit
    global upscaler1
    global upscaler2
    global cfg_scale
    global width
    global height
    global temp_path_upscale
    global temp_var_edit
    global temp_var_edit_upscale
    global live_img_update_id
    global temp_var_edit_model
    global temp_var_edit_setting
    global temp_var_edit_setting_mota
    global user_id_list
    global global_id_timer_del
    global global_id_timer
    global timmer

###############################################################################################################
########################################## SPAM################################################################

    randomemoff = ['CAACAgUAAxkBAAEc8uBj47KXuBsM1Ow8Ut63GwH0iEe0kAACiAcAApImIFcMOgL6w2Pp7y4E',
                   'CAACAgUAAxkBAAEc8uZj47LCxLSrZvgVGtIZflJEHd9SzAAC5wcAAvW5yFY0Q-G6KJDlIC4E', 'CAACAgUAAxkBAAEc8upj47NAGDBva4ycgmu6AtvYz0Lz3AACVQcAAmwPyFYnV6RK0L1DkS4E']
    if (query.data) in ["1", "2", "3", "x"]:
        print("LOG | SPAM STICKER: CALLED")
        for i in range(spamcout):
            time.sleep(0.2)
            if (query.data == "x"):
                context.bot.send_sticker(
                    chat_id=query.message.chat_id, sticker=random.choice(randomemoff))
            else:
                context.bot.send_sticker(
                    chat_id=query.message.chat_id, sticker=randomemoff[int(query.data)-1])


###############################################################################################################
########################################## TKB################################################################

    elif (query.data) == "stop":
        global stoptkb
        if check_if_in_study_time():
            stoptkb[listidtkb.index(str(query.message.chat_id))] = True
            print("LOG | LEASSON ALLERT: Stopped")
            context.bot.sendMessage(
                text="Đã dừng thông báo!", chat_id=query.message.chat_id)
        else:
            context.bot.sendMessage(
                text="Không có thông báo đang gửi!", chat_id=query.message.chat_id)

    elif (query.data) in ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ nhật", "full", "tkbnow", "tkbtmr"]:
        if (query.data) == "full":
            for i in range(7):
                if leasson_allert.magic5(i) != "":
                    context.bot.sendMessage(text=leasson_allert.magic5(
                        i), chat_id=query.message.chat_id, parse_mode="MarkdownV2")
            context.bot.send_sticker(chat_id=query.message.chat_id,
                                     sticker="CAACAgIAAxkBAAEfPwNkLBzQMRhJOheeKBuVLDh0Le5cwAACP0AAAuCjggdy3Jqkup9_-y8E")
        elif (query.data) == "tkbnow":
            a = leasson_allert.magic2()
            if ((a != '\!\!del learn\!\! ze zeeeee\!\!\!\!\!') and (leasson_allert.magic2() != None)):
                context.bot.sendMessage(
                    text=a, chat_id=query.message.chat_id, parse_mode="MarkdownV2")
            else:
                context.bot.sendMessage(text="Hiện tại không có môn nào sắp vào học \!",
                                        chat_id=query.message.chat_id, parse_mode="MarkdownV2")
        elif (query.data) == "tkbtmr":
            context.bot.sendMessage(text=leasson_allert.magic5(int(date.today(
            ).weekday())+1), chat_id=query.message.chat_id, parse_mode="MarkdownV2")
        else:
            if query.data != "Chủ nhật":
                A = leasson_allert.magic5(int(query.data[4:])-2)
            else:
                A = leasson_allert.magic5(6)
            if A == "":
                context.bot.sendMessage(
                    text=query.data+" không có học 🤗", chat_id=query.message.chat_id, parse_mode="MarkdownV2")
            else:
                context.bot.sendMessage(
                    text=A, chat_id=query.message.chat_id, parse_mode="MarkdownV2")

    elif "bard_" in query.data:
        callback_history_text = "bard_chat/" + \
            str(query.message.chat_id) + "_h.json"
        with open(callback_history_text, 'r', encoding="utf-8") as json_file:
            data = json.load(json_file)
        buttons = []
        with open(callback_history_text, "w",  encoding="utf-8") as f:
            json.dump({'conversation_id': data['conversation_id'],
                       'response_id': data['response_id'],
                       'choice_id': data['repon_mess']['choices'][int(query.data[5:])]['id'],
                       'last_mess_id': data['last_mess_id'],
                       'repon_mess': data['repon_mess']}, f)

        for i in range(len(data['repon_mess']['choices'])):
            if i == int(query.data[5:]):
                buttons.append(InlineKeyboardButton(
                    str(i+1)+' ⏺️', callback_data="bard_" + str(i)))
            else:
                buttons.append(InlineKeyboardButton(
                    str(i+1)+' ⬜', callback_data="bard_" + str(i)))
        context.bot.editMessageText(reply_markup=InlineKeyboardMarkup([buttons]), message_id=str(data['last_mess_id']), chat_id=query.message.chat_id, text=a_cat_lying_on_the_sand.escape(
            data['repon_mess']['choices'][int(query.data[5:])]['content'][0]), parse_mode="MarkdownV2")


###############################################################################################################
########################################## DRAW################################################################
    elif (("variable" in query.data) or ("upscale" in query.data)) and (query.message.chat_id not in user_id_list):
        user_id_list.append(query.message.chat_id)

    elif ("pnginfo" in query.data):
        info = json.loads(a_cat_lying_on_the_sand.getinfoimage(
            os.path.join('stable_diffusion', query.data[7:])))
        del info["Seed resize from"]
        del info["Denoising strength"]
        del info["Model hash"]
        new_str = "\n".join(
            [f'<b>{key}</b>: <code>{value.replace("<","&lt;").replace(">","&gt;")}</code>' for key, value in info.items()])
        context.bot.sendMessage(
            chat_id=query.message.chat_id, text=new_str, parse_mode="HTML")

    elif (len(user_id_list) > 0) and (user_id_list[0] == query.message.chat_id):
        if "settingdraw" == (query.data):
            timmer = sec_timer
            buttons = [[InlineKeyboardButton("Cài đặt model 📄", callback_data="setmodeldraw")], [InlineKeyboardButton("Mô tả model 📜", callback_data="mota")], [InlineKeyboardButton("Cài đặt steps 🪜", callback_data="settingsteps")], [
                InlineKeyboardButton("Cài đặt Sampling method 🌴", callback_data="settingsampler")], [InlineKeyboardButton("Cài đặt seeds 🌱", callback_data="settingseeds")], [InlineKeyboardButton("Cài đặt cfg scale 🤥", callback_data="settingcfg")]]
            a = temp_var_edit_setting.message_id
            temp_var_edit_setting = context.bot.editMessageText(message_id=a, reply_markup=InlineKeyboardMarkup(buttons), chat_id=user_id_list[0], text="<b>Cài đặt hiện tại:</b>\n\n<b>Model:</b> <code>"+a_cat_lying_on_the_sand.get_model()+"</code>\n<b>Steps:</b> <code>"+str(
                steps)+"</code>\n<b>Seeds:</b> <code>"+str(seeds)+"</code>\n<b>Sampling method:</b> <code>"+sampling_method + "</code>\n<b>Cfg scale:</b> <code>" + str(cfg_scale)+"</code>\n\nCậu chọn chức năng cần chỉnh sửa nha:", parse_mode="HTML")

        elif "mota" in (query.data):
            timmer = sec_timer
            buttons = []
            modelall = a_cat_lying_on_the_sand.get_all_model()
            for i in range(len(modelall)):
                buttons.append([InlineKeyboardButton(
                    modelall[i], callback_data="mot\@" + str(i))])
            buttons.append([InlineKeyboardButton(
                "Quay lại 🔙", callback_data="settingdraw")])
            if query.data[-1] == "1":
                context.bot.deleteMessage(
                    message_id=temp_var_edit_setting_mota.message_id, chat_id=user_id_list[0])
                temp_var_edit_setting = temp_var_edit_setting_mota = context.bot.sendMessage(reply_markup=InlineKeyboardMarkup(
                    buttons), chat_id=user_id_list[0], text="Chọn model muốn bé mô tả nka\!\!\!📃📜📄", parse_mode="MarkdownV2")
            if query.data == "mota":
                temp_var_edit_setting = temp_var_edit_setting_mota = context.bot.editMessageText(message_id=temp_var_edit_setting.message_id, reply_markup=InlineKeyboardMarkup(
                    buttons), chat_id=user_id_list[0], text="Chọn model muốn bé mô tả nka\!\!\!📃📜📄", parse_mode="MarkdownV2")

        elif ("mot\@" in query.data):
            timmer = sec_timer
            listmodel = a_cat_lying_on_the_sand.get_all_model("title")
            buttons = [[InlineKeyboardButton(
                "Quay lại 🔙", callback_data="mota1")]]
            try:
                context.bot.deleteMessage(
                    message_id=temp_var_edit_setting_mota.message_id, chat_id=user_id_list[0])
            except:
                pass
            # context.bot.editMessageText(message_id =temp_var_edit_setting.message_id,chat_id=user_id_list[0], text=)
            context.bot.send_chat_action(
                chat_id=user_id_list[0], action=ChatAction.UPLOAD_PHOTO)
            temp_var_edit_setting_mota = context.bot.send_photo(reply_markup=InlineKeyboardMarkup(buttons), chat_id=user_id_list[0], caption="<b>"+listmodel[int(query.data[5:])]+"</b>"+"\n\n"+motaJson[listmodel[int(query.data[5:])]][0] + "\n\nCậu có thể thử mẫu này nka: " + "<code>" + motaJson[listmodel[int(query.data[5:])]][1] + "</code>" + "\nSteps là: " + "<code>" + motaJson[listmodel[int(query.data[5:])]][2] + "</code>" + "\nSeed là: "+"<code>" + motaJson[listmodel[int(query.data[5:])]][3] + "</code>" + "\nSampler là " + "<code>" + motaJson[listmodel[int(query.data[5:])]][4] + "</code>" + "\nCfg scale là " + "<code>" + motaJson[listmodel[int(query.data[5:])]][6] + "</code>", parse_mode="HTML",
                                                                photo=open(os.path.join('anhmotamodel', motaJson[listmodel[int(query.data[5:])]][5]), 'rb'))

        elif "setmodeldraw" in (query.data):
            timmer = sec_timer
            buttons = []
            modelall = a_cat_lying_on_the_sand.get_all_model()
            for i in range(len(modelall)):
                buttons.append([InlineKeyboardButton(
                    modelall[i], callback_data="dmbm" + str(i))])
            buttons.append([InlineKeyboardButton(
                "Quay lại 🔙", callback_data="settingdraw")])
            a = temp_var_edit_setting.message_id
            temp_var_edit_model = context.bot.editMessageText(message_id=a, reply_markup=InlineKeyboardMarkup(
                buttons), chat_id=user_id_list[0], text="Chọn model hình ảnh 🌃🌃🌃", parse_mode="MarkdownV2")

        elif ("dmbm" in query.data):
            timmer = sec_timer
            listmodel = a_cat_lying_on_the_sand.get_all_model("title")
            context.bot.editMessageText(
                chat_id=user_id_list[0], text="Chờ tớ xíu...", message_id=temp_var_edit_model.message_id)
            buttons = [[InlineKeyboardButton(
                "Xong rồi nèk 😊", callback_data="settingdraw")]]
            if a_cat_lying_on_the_sand.set_model(listmodel[int(query.data[4:])]):
                context.bot.editMessageText(reply_markup=InlineKeyboardMarkup(buttons), chat_id=temp_var_edit_model.chat.id,
                                            message_id=temp_var_edit_model.message_id, text="Đã set model thành "+listmodel[int(query.data[4:])])
            timmer = sec_timer
        elif "settingsteps" in (query.data):
            timmer = sec_timer
            buttons = [[InlineKeyboardButton(
                "Quay lại 🔙", callback_data="settingdraw")]]
            context.bot.editMessageText(reply_markup=InlineKeyboardMarkup(buttons), message_id=temp_var_edit_setting.message_id, chat_id=user_id_list[0],
                                        text="Nhắn em `/steps + số lượng` nhé \nVd như `/steps 20` 😎 \nCâu lưu ý thuộc tính này chỉ từ 1 tới 150 thôi nka 😊😊😊", parse_mode="MarkdownV2")
        elif "settingseeds" in (query.data):
            timmer = sec_timer
            buttons = [[InlineKeyboardButton(
                "Quay lại 🔙", callback_data="settingdraw")]]
            context.bot.editMessageText(reply_markup=InlineKeyboardMarkup(buttons), message_id=temp_var_edit_setting.message_id, chat_id=user_id_list[0],
                                        text="Nhắn em `/seeds + số lượng` nhé \nVd như `/seeds 20` \nNhắn em `/seeds \-1` để random 🌱️🌱️🌱️", parse_mode="MarkdownV2")
        elif "settingcfg" in (query.data):
            timmer = sec_timer
            buttons = [[InlineKeyboardButton(
                "Quay lại 🔙", callback_data="settingdraw")]]
            context.bot.editMessageText(reply_markup=InlineKeyboardMarkup(buttons), message_id=temp_var_edit_setting.message_id, chat_id=user_id_list[0],
                                        text="Nhắn em `/cfg + số` nka \nVd như `/cfg 7` 🤭 \nCâu lưu ý thuộc tính này chỉ từ 1 tới 30 thôi nka 😊😊😊", parse_mode="MarkdownV2")
        elif "settingsampler" in (query.data):
            timmer = sec_timer
            buttons = []
            allsampler = a_cat_lying_on_the_sand.get_all_sampler()
            for i in range(0, len(allsampler)-(len(allsampler) % 3), 3):
                buttons.append([InlineKeyboardButton(allsampler[i], callback_data="samplerr" + str(i)), InlineKeyboardButton(allsampler[i+1],
                                                                                                                             callback_data="samplerr" + str(i+1)), InlineKeyboardButton(allsampler[i+2], callback_data="samplerr" + str(i+2))])
            if len(allsampler) % 3 == 1:
                buttons.append([InlineKeyboardButton(allsampler[len(
                    allsampler)-1], callback_data="samplerr" + str(len(allsampler)-1))])
            elif len(allsampler) % 3 == 2:
                buttons.append([InlineKeyboardButton(allsampler[len(allsampler)-2], callback_data="samplerr" + str(len(allsampler)-2)),
                                InlineKeyboardButton(allsampler[len(allsampler)-1], callback_data="samplerr" + str(len(allsampler)-1))])
            buttons.append([InlineKeyboardButton(
                "Quay lại 🔙", callback_data="settingdraw")])
            temp_var_edit = context.bot.editMessageText(message_id=temp_var_edit_setting.message_id, reply_markup=InlineKeyboardMarkup(
                buttons), chat_id=user_id_list[0], text="Chọn Sampling method 🥶️🥶️🥶️", parse_mode="MarkdownV2")
        elif ("samplerr" in query.data):
            timmer = sec_timer
            sampling_method = a_cat_lying_on_the_sand.get_all_sampler()[
                int(query.data[8:])]
            buttons = [[InlineKeyboardButton(
                "Xong rồi nèk 😊", callback_data="settingdraw")]]

            context.bot.editMessageText(reply_markup=InlineKeyboardMarkup(buttons), chat_id=user_id_list[0],
                                        text="Đã chỉnh sampling method thành: "+sampling_method, message_id=temp_var_edit.message_id)

        elif "drawaimagevippro" in (query.data):
            timmer = sec_timer
            context.bot.deleteMessage(message_id=temp_var_delete.message_id,
                                      chat_id=live_img_update_id)

            print("LOG | STABLE DIFFUSION PROMPT: "+fntext)
            print("LOG | STABLE DIFFUSION NEGATIVE PROMPT: " + fnnvtext)
            isit = True
            # set size:
            if query.data[16:] == "1":
                width = 512
                height = 512
            elif query.data[16:] == "2":
                width = 800
                height = 400
            elif query.data[16:] == "3":
                width = 400
                height = 800
            # ---------------------------

            a = a_cat_lying_on_the_sand.drawstb(
                fntext, fnnvtext, steps, sampling_method, seeds, cfg_scale, width, height)
            buttons = [[InlineKeyboardButton("Biến thể 😮", callback_data="variable"+str(a[17:])), InlineKeyboardButton(
                "Upscale 🤤", callback_data="upscale"+str(a[17:]))], [InlineKeyboardButton("Thông tin chi tiết 📑", callback_data="pnginfo"+str(a[17:]))]]
            context.bot.send_chat_action(
                chat_id=user_id_list[0], action=ChatAction.UPLOAD_PHOTO)
            context.bot.send_photo(reply_markup=InlineKeyboardMarkup(
                buttons), chat_id=user_id_list[0], photo=open(a, 'rb'))
            isit = False
            context.bot.deleteMessage(message_id=temp_var_delete_1.message_id,
                                      chat_id=live_img_update_id)
            print("LOG | STABLE DIFFUSION: Done")
            print('LOG | STABLE DIFFUSION:',a[17:])

            if len(user_id_list) > 1:
                # finish
                context.bot.sendMessage(
                    chat_id=user_id_list[0], text="Xong rồi nhá, nếu muốn tớ giúp thì ráng đợi những bạn khác nha 🥹🥹🥹")
                context.bot.send_sticker(
                    chat_id=user_id_list[0], sticker='CAACAgIAAxkBAAEfPYJkLAHQ9KtOv4G_5HddERkJLNe1qgACT0AAAuCjggcuO1Eat5jdpy8E')

                user_id_list.pop(0)
                timmer = sec_timer
                # next user
                global_id_timer = context.bot.sendMessage(
                    chat_id=user_id_list[0], text="Tới cậu rùi nè!!! Hãy nhắn tớ nha, chờ cậu áaa 🤭🤭🤭")
                global_id_timer_del = context.bot.send_sticker(
                    chat_id=user_id_list[0], sticker='CAACAgIAAxkBAAEfPVVkK_4_XpLGVB-QDt_gOzDio8KRCwACuD8AAuCjggeu6M3W5FneWy8E')

            else:
                # global_id_timer =  context.bot.sendMessage(chat_id=user_id_list[0], text="Còn mỗi cậu à, nhắn tớ tiếp nha!!! 🥺🥺🥺")
                # global_id_timer_del = context.bot.send_sticker(
                #     chat_id=user_id_list[0], sticker='CAACAgIAAxkBAAEfPvNkLBvTeEq4Wlb6XRPTwLKlYwY4YwAC6koAAuCjggcjPrpyUZMvHS8E')
                timmer = sec_timer

        elif ("variable" in query.data):
            timmer = sec_timer
            if query.data[:9] == "1variable":
                print('LOG | STABLE DIFFUSION:',query.data[9:])
                live_img_update_id = user_id_list[0]

                isit = True
                a = a_cat_lying_on_the_sand.img2img(os.path.join('stable_diffusion', query.data[9:]), fntext, fnnvtext,
                                                    steps, sampling_method, -1, cfg_scale, 512,  512)
                buttons = [[InlineKeyboardButton("Biến thể 😮", callback_data="variable"+str(a[17:])), InlineKeyboardButton(
                    "Upscale 🤤", callback_data="upscale"+str(a[17:]))], [InlineKeyboardButton("Thông tin chi tiết 📑", callback_data="pnginfo"+str(a[17:]))]]
                context.bot.send_chat_action(
                    chat_id=user_id_list[0], action=ChatAction.UPLOAD_PHOTO)
                context.bot.send_photo(caption="*Biến thể* của `Ảnh gửi lên`\nSeed: `" + json.loads(a_cat_lying_on_the_sand.getinfoimage(a))[
                    'Seed']+"`", reply_markup=InlineKeyboardMarkup(buttons), chat_id=user_id_list[0], photo=open(a, 'rb'), parse_mode="MarkdownV2")
                isit = False
                context.bot.deleteMessage(message_id=temp_var_delete_1.message_id,
                                          chat_id=live_img_update_id)
                print("LOG | STABLE DIFFUSION: Done")
                print('LOG | STABLE DIFFUSION:',a[17:])

            else:
                print('LOG | STABLE DIFFUSION:',query.data[8:])
                live_img_update_id = user_id_list[0]
                pnginfo = json.loads(a_cat_lying_on_the_sand.getinfoimage(
                    os.path.join('stable_diffusion', query.data[8:])))
                if 'Negative prompt' in pnginfo:
                    Negative_prompt = pnginfo['Negative prompt']
                else:
                    Negative_prompt = ""

                isit = True
                a = a_cat_lying_on_the_sand.img2img(os.path.join('stable_diffusion', query.data[8:]), pnginfo['Prompt'], Negative_prompt,
                                                    steps, sampling_method, -1, cfg_scale, pnginfo['Size'].split('x')[0],  pnginfo['Size'].split('x')[1])
                buttons = [[InlineKeyboardButton("Biến thể 😮", callback_data="variable"+str(a[17:])), InlineKeyboardButton(
                    "Upscale 🤤", callback_data="upscale"+str(a[17:]))], [InlineKeyboardButton("Thông tin chi tiết 📑", callback_data="pnginfo"+str(a[17:]))]]
                context.bot.send_chat_action(
                    chat_id=user_id_list[0], action=ChatAction.UPLOAD_PHOTO)
                context.bot.send_photo(caption="*Biến thể* của `"+pnginfo["Seed"]+"`\nSeed: `" + json.loads(a_cat_lying_on_the_sand.getinfoimage(a))[
                    'Seed']+"`", reply_markup=InlineKeyboardMarkup(buttons), chat_id=user_id_list[0], photo=open(a, 'rb'), parse_mode="MarkdownV2")
                isit = False
                context.bot.deleteMessage(message_id=temp_var_delete_1.message_id,
                                          chat_id=live_img_update_id)
                print("LOG | STABLE DIFFUSION: Done")
                print('LOG | STABLE DIFFUSION:',a[17:])

                if len(user_id_list) > 1:
                    # finish
                    context.bot.sendMessage(
                        chat_id=user_id_list[0], text="Xong rồi nhá, nếu muốn tớ giúp thì ráng đợi những bạn khác nha 🥹🥹🥹")
                    context.bot.send_sticker(
                        chat_id=user_id_list[0], sticker='CAACAgIAAxkBAAEfPYJkLAHQ9KtOv4G_5HddERkJLNe1qgACT0AAAuCjggcuO1Eat5jdpy8E')

                    user_id_list.pop(0)
                    # next user
                    global_id_timer = context.bot.sendMessage(
                        chat_id=user_id_list[0], text="Tới cậu rùi nè!!! Hãy nhắn tớ nha, chờ cậu áaa 🤭🤭🤭")
                    global_id_timer_del = context.bot.send_sticker(
                        chat_id=user_id_list[0], sticker='CAACAgIAAxkBAAEfPVVkK_4_XpLGVB-QDt_gOzDio8KRCwACuD8AAuCjggeu6M3W5FneWy8E')
                    timmer = sec_timer
                else:
                    # global_id_timer =  context.bot.sendMessage(chat_id=user_id_list[0], text="Còn mỗi cậu à, nhắn tớ tiếp nha!!! 🥺🥺🥺")
                    # global_id_timer_del= context.bot.send_sticker(
                    #     chat_id=user_id_list[0], sticker='CAACAgIAAxkBAAEfPvNkLBvTeEq4Wlb6XRPTwLKlYwY4YwAC6koAAuCjggcjPrpyUZMvHS8E')
                    timmer = sec_timer

        elif ("upscale" in query.data):
            timmer = sec_timer
            buttons = []
            print('LOG | STABLE DIFFUSION:',query.data[7:])
            temp_path_upscale = query.data[7:]
            upscaler_all = a_cat_lying_on_the_sand.get_all_upscaler()
            for i in range(0, len(upscaler_all)-(len(upscaler_all) % 2), 2):
                buttons.append([InlineKeyboardButton(upscaler_all[i], callback_data="upscalir1+"+str(
                    i)), InlineKeyboardButton(upscaler_all[i+1], callback_data="upscalir1+" + str(i+1))])
            if len(upscaler_all) % 2 == 1:
                buttons.append([InlineKeyboardButton(upscaler_all[len(
                    upscaler_all)-1], callback_data="upscalir1+"+str(len(upscaler_all)-1))])

            temp_var_edit_upscale = context.bot.sendMessage(reply_markup=InlineKeyboardMarkup(
                buttons), chat_id=user_id_list[0], text="Chọn model *upscaler 1* nka \!\!\!", parse_mode="MarkdownV2")

        elif ("upscalir1+" in query.data):
            timmer = sec_timer
            upscaler_all = a_cat_lying_on_the_sand.get_all_upscaler()
            buttons = []
            upscaler1 = a_cat_lying_on_the_sand.get_all_upscaler()[
                int(query.data[10:])]
            print("LOG | STABLE DIFFUSION: CALLED UPSCALE")
            print('LOG | STABLE DIFFUSION:',query.data[10:])

            for i in range(0, len(upscaler_all)-(len(upscaler_all) % 2), 2):
                buttons.append([InlineKeyboardButton(upscaler_all[i], callback_data="upscalir2+"+str(
                    i)), InlineKeyboardButton(upscaler_all[i+1], callback_data="upscalir2+" + str(i+1))])
            if len(upscaler_all) % 2 == 1:
                buttons.append([InlineKeyboardButton(upscaler_all[len(
                    upscaler_all)-1], callback_data="upscalir2+"+str(len(upscaler_all)-1))])
            a = temp_var_edit_upscale
            temp_var_edit_upscale = context.bot.editMessageText(message_id=a.message_id, reply_markup=InlineKeyboardMarkup(
                buttons), chat_id=user_id_list[0], text="Model <b> upscaler 1 là: "+upscaler1+"</b>\nChọn model <b>upscaler 2</b> nka !!! 😮", parse_mode="HTML")

        elif ("upscalir2+" in query.data):
            print('LOG | STABLE DIFFUSION:',query.data[10:])
            timmer = sec_timer*10
            context.bot.send_chat_action(
                chat_id=user_id_list[0], action=ChatAction.UPLOAD_DOCUMENT)
            upscaler_all = a_cat_lying_on_the_sand.get_all_upscaler()
            upscaler2 = a_cat_lying_on_the_sand.get_all_upscaler()[
                int(query.data[10:])]
            context.bot.deleteMessage(message_id=temp_var_edit_upscale.message_id,
                                      chat_id=user_id_list[0])
            result_path = a_cat_lying_on_the_sand.upscale_img(
                upscaler1, upscaler2, os.path.join('stable_diffusion', temp_path_upscale))
            context.bot.send_chat_action(
                chat_id=user_id_list[0], action=ChatAction.UPLOAD_DOCUMENT)
            context.bot.sendDocument(caption="Ảnh đã được tớ làm rõ ròi nèeeee ☺️",
                                     chat_id=user_id_list[0], document=open(result_path, 'rb'))

            if len(user_id_list) > 1:
                # finish
                context.bot.sendMessage(
                    chat_id=user_id_list[0], text="Xong rồi nhá, nếu muốn tớ giúp thì ráng đợi những bạn khác nha 🥹🥹🥹")
                context.bot.send_sticker(
                    chat_id=user_id_list[0], sticker='CAACAgIAAxkBAAEfPYJkLAHQ9KtOv4G_5HddERkJLNe1qgACT0AAAuCjggcuO1Eat5jdpy8E')

                user_id_list.pop(0)
                # next user
                global_id_timer = context.bot.sendMessage(
                    chat_id=user_id_list[0], text="Tới cậu rùi nè!!! Hãy nhắn tớ nha, chờ cậu áaa 🤭🤭🤭")
                global_id_timer_del = context.bot.send_sticker(
                    chat_id=user_id_list[0], sticker='CAACAgIAAxkBAAEfPVVkK_4_XpLGVB-QDt_gOzDio8KRCwACuD8AAuCjggeu6M3W5FneWy8E')
                timmer = sec_timer
            else:
                # global_id_timer =  context.bot.sendMessage(chat_id=user_id_list[0], text="Còn mỗi cậu à, nhắn tớ tiếp nha!!! 🥺🥺🥺")
                # global_id_timer_del = context.bot.send_sticker(
                #     chat_id=user_id_list[0], sticker='CAACAgIAAxkBAAEfPvNkLBvTeEq4Wlb6XRPTwLKlYwY4YwAC6koAAuCjggcjPrpyUZMvHS8E')
                timmer = sec_timer

    elif (len(user_id_list) < 0) or (user_id_list[0] != query.message.chat_id):
        context.bot.sendMessage(chat_id=query.message.chat_id, text="Cậu đang đứng thứ <b>" + str(user_id_list.index(update.message.chat_id) + 1) +
                                "</b> trong hàng chờ cùng <span class='tg-spoiler'>" + str(random.randint(1000000000, 99999999999)) + "</span> người khác, ráng chờ lát nha 🤥🤭🤥", parse_mode="HTML")
        context.bot.send_sticker(
            chat_id=query.message.chat_id, sticker='CAACAgIAAxkBAAEfPB5kK-t41_kYFuqoEb1wOP7bJDTeVAACuj8AAuCjggcykMz6vc920i8E')


# Log errors


def error(update, context):
    print(f'LOG | TELEGARM: Update {update} caused error {context.error}')


classdh = "KTPM0121"


def tkb_command(update, context):
    text = str(update.message.text).lower()
    if text == "/tkb" or text == "/tkb@randomfoodruribot":
        buttons = [[KeyboardButton(
            "/tkb print")], [KeyboardButton("/tkb reg")], [KeyboardButton("/tkb unreg")]]
        update.message.reply_text(reply_markup=ReplyKeyboardMarkup(
            buttons), text="Cậu có thể dùng lệnh `/tkb print` để xem toàn bộ thời khoá biểu trong tuần 🌞\nHoặc dùng lệnh `/tkb reg` để đăng ký nhận thông báo môn học trước 1 tiếng từ tớ nha 😘", parse_mode="MarkdownV2")
    if "/tkb" in text:
        text = text.replace('/tkb', '').strip()
    print('LOG | LEASSON ALLERT:',text)
    if text == "print":
        buttons = [[InlineKeyboardButton("Sắp học 🫥", callback_data="tkbnow")], [InlineKeyboardButton("Ngày mai 😮", callback_data="tkbtmr")], [InlineKeyboardButton("Thứ 2 🤨", callback_data="Thứ 2")], [InlineKeyboardButton("Thứ 3 🌞", callback_data="Thứ 3")], [InlineKeyboardButton("Thứ 4 🥹", callback_data="Thứ 4")], [
            InlineKeyboardButton("Thứ 5 😙", callback_data="Thứ 5")], [InlineKeyboardButton("Thứ 6 😍", callback_data="Thứ 6")], [InlineKeyboardButton("Thứ 7 🤗", callback_data="Thứ 7")], [InlineKeyboardButton("Chủ nhật ❤️", callback_data="Chủ nhật")], [InlineKeyboardButton("Toàn bộ tkb 🤤", callback_data="full")]]
        update.message.reply_text(text="Chọn ngày thời khoá biểu cậu muốn đi 😶‍🌫️",
                                  parse_mode="MarkdownV2", reply_markup=InlineKeyboardMarkup(buttons))

    if text == "reg":
        if str(update.message.chat.id) not in listidtkb:
            f = open("tkb.txt", "a", encoding="utf-8")
            f.write(str(update.message.chat.id)+"\n")
            f.close()
            startup()
            update.message.reply_text(
                text="Bạn đã đăng kí nhận thông báo lịch học của lớp "+classdh+" thành công\!", parse_mode="MarkdownV2")
        else:
            update.message.reply_text(
                text="Bạn hiện nằm trong danh sách thông báo lịch học lớp "+classdh+"\!", parse_mode="MarkdownV2")

    if text == "unreg":
        if str(update.message.chat.id) in listidtkb:
            listidtkb.remove(str(update.message.chat.id))
            if os.path.exists("tkb.txt"):
                os.remove("tkb.txt")
            f = open("tkb.txt", "a", encoding="utf-8")
            for i in listidtkb:
                f.write(i+"\n")
            f.close()
            startup()
            update.message.reply_text(
                text="Bạn huỷ đăng kí nhận thông báo lịch học của lớp "+classdh+" thành công\!", parse_mode="MarkdownV2")
        else:
            update.message.reply_text(
                text="Bạn hiện không nằm trong danh sách thông báo lịch học lớp "+classdh+"\!", parse_mode="MarkdownV2")


checkdebug = False


def debug_command(update, context):
    global checkdebug
    text = str(update.message.text).lower()
    if (text == "/debug") or (text == "/debug@randomfoodruribot"):
        update.message.reply_text(
            text="Mở debug?\nNhập `/debug + pass`\! 😬", parse_mode="MarkdownV2")
    elif (text == "/debug 18102003") or (text == "/debug@randomfoodruribot 18102003"):
        checkdebug = True
        buttons = [[KeyboardButton("/debug cookie tkb")], [KeyboardButton(
            "/debug reboot")], [KeyboardButton("/debug url")], [KeyboardButton("/debug logout")]]
        update.message.reply_text(
            reply_markup=ReplyKeyboardMarkup(buttons), text="done")
    elif (text == "/debug cookie tkb") or (text == "/debug@randomfoodruribot cookie tkb"):
        if checkdebug:
            update.message.reply_text(
                text="Gửi cokie mới qua câu lệnh `/debug set cookie + cookie`\nLưu ý sau khi set cookie", parse_mode="MarkdownV2")
        else:
            update.message.reply_text(text="Không có quyền")
    elif (text == "/debug url") or (text == "/debug@randomfoodruribot url"):
        if checkdebug:
            update.message.reply_text(
                text="Gửi url mới qua câu lệnh `/debug set url + url`", parse_mode="MarkdownV2")
        else:
            update.message.reply_text(text="Không có quyền")
    elif (text == "/debug reboot") or (text == "/debug@randomfoodruribot reboot"):
        if checkdebug:
            update.message.reply_text(text="Lệnh được thực thi! 🌫️")
            os.system("sudo reboot")
        else:
            update.message.reply_text(text="Không có quyền")

    elif (text == "/debug logout") or (text == "/debug@randomfoodruribot logout"):
        update.message.reply_text(text="Lệnh được thực thi! 🌫️")
        checkdebug = False
    elif ("/debug set cookie" in text):
        if checkdebug:
            text = text.replace('/debug set cookie', '').strip()
            with open('credentials-user.json', 'r') as file:
                data = json.load(file)
            data['ASC.AUTH'] = text
            with open('credentials-user.json', 'w') as file:
                json.dump(data, file)
            update.message.reply_text(text="Lệnh được thực thi! 🌫️")
            leasson_allert.reloadcookie()
            startup()
        else:
            update.message.reply_text(text="Không có quyền")
    elif ("/debug set url" in text):
        if checkdebug:
            text = text.replace('/debug set url', '').strip()
            with open('credentials-user.json', 'r') as file:
                data = json.load(file)
            data['url'] = text
            with open('credentials-user.json', 'w') as file:
                json.dump(data, file)
            update.message.reply_text(text="Lệnh được thực thi! 🌫️")
            a_cat_lying_on_the_sand.reloadlink()
            startup()
        else:
            update.message.reply_text(text="Không có quyền")
    else:
        update.message.reply_text(text="Sai pass! ⛔")


def null_command(update, context):
    text = str(update.message.text).lower()
    if text == "/null" or text == "/null@randomfoodruribot":
        context.bot.send_video(chat_id=update.message.chat_id, video=open(
            'vid/yeah.mp4', 'rb'), supports_streaming=True)


modelgpt = "gpt-3.5-turbo"
settemp = 0.5

isit = False


def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301"):
    encoding = tiktoken.encoding_for_model(model)
    num_tokens = 0
    for message in messages:
        # every message follows <im_start>{role/name}\n{content}<im_end>\n
        num_tokens += 4
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":  # if there's a name, the role is omitted
                num_tokens += -1  # role is always required and always 1 token
    num_tokens += 2  # every reply is primed with <im_start>assistant
    return num_tokens


def gpt_command(update, context):
    global modelgpt
    global settemp
    global max_tokens
    history_text = "gpt_chat/"+str(update.message.chat.id) + "_h.json"
    if not os.path.isfile(history_text):
        with open(history_text, "w",  encoding="utf-8") as f:
            json.dump(
                {"role": "system", "content": "Assistant is a large language model trained by OpenAI."}, f)
    else:
        print("LOG | GPT: Log have been created")
    text = str(update.message.text).lower()
    if text == "/gpt" or text == "/gpt@randomfoodruribot":
        buttons = [[KeyboardButton("/gpt clear")],
                   [KeyboardButton("/gpt settemp")]]
        update.message.reply_text(reply_markup=ReplyKeyboardMarkup(
            buttons), text="Nhắn em `/gpt + tin nhắn` để nhắn với tính cách gpt nhé 😊\nĐổi độ sáng tạo bằng `/gpt settemp [số 0-1]` số càng gần 1 thì nội dung phong phú khó đoán, số bé khi muốn câu trả lời chính xác 😊\nDùng lệnh `/gpt clear` để xoá lịch sử chat 😶‍🌫️\nNếu bot không phản hồi gì thì hãy thử dùng lệnh `/gpt clear` nhé ☺️", parse_mode="MarkdownV2")
        context.bot.sendMessage(chat_id=update.message.chat.id, text="Mô hình hiện tại là <code>" +
                                modelgpt + "</code>\nĐộ sáng tạo là <code>"+str(settemp)+"</code>", parse_mode="HTML")

    elif "/gpt settemp" in text or "/gpt@randomfoodruribot settemp" in text:
        text = text.replace(
            "/gpt settemp ", "").replace("/gpt@randomfoodruribot settemp ", "")
        if text.replace('.', '', 1).isnumeric():
            settemp = float(text)
            context.bot.sendMessage(chat_id=update.message.chat.id,
                                    text="Đã chỉnh độ sáng tạo là `" + text + "`", parse_mode="MarkdownV2")
        else:
            context.bot.sendMessage(chat_id=update.message.chat.id,
                                    text="Lỗi cú pháp, cậu hãy nhắn như ví dụ này `/gpt settemp 0.3`", parse_mode="MarkdownV2")

    elif text == "/gpt clear" or text == "/gpt@randomfoodruribot clear":
        try:
            os.remove(history_text)
        except:
            print("LOG | GPT: Idk but cant clear log")
        context.bot.sendMessage(
            chat_id=update.message.chat.id, text="Đã xoá lịch sử chat với GPT 😊")

    else:
        context_bot.bot.send_chat_action(
            chat_id=update.message.chat.id, action=ChatAction.TYPING)
        text = text.replace("/gpt", "").replace("/gpt@randomfoodruribot", "")

        with open(history_text, 'r') as json_file:
            data = json.load(json_file)
        data_list = [data]
############## fixlist########################
        new_list = []
        for item in data_list:
            if isinstance(item, list):
                new_list.extend(item)
            else:
                new_list.append(item)
        data_list = new_list
        del new_list
############## fixlist########################
        data_list.append({"role": "user", "content": text})
        conv_history_tokens = num_tokens_from_messages(data_list)
        print('LOG | GPT:',conv_history_tokens)
        hiccc = False
        while (conv_history_tokens+1000 >= 4096):
            hiccc = True
            del data_list[1]
            conv_history_tokens = num_tokens_from_messages(data_list)

        if hiccc:
            context.bot.sendMessage(chat_id=update.message.chat.id,
                                    text="<b>Đạt giới hạn token, một vài ký ức đã bị mất đi...</b>", ParseMode="HTML")

        response = openai.ChatCompletion.create(
            model=modelgpt,
            messages=data_list,
            temperature=settemp,
            max_tokens=1000,
        )
        if response['choices'][0]['message']['content'] == "" or response['choices'][0]['message']['content'] == None:
            context.bot.sendMessage(chat_id=update.message.chat.id,
                                    text="Replika: Em xin lỗi nhưng có vẻ nhân cách GPT không phản hồi bất cứ thứ gì cả 🥹")
        else:
            context.bot.sendMessage(
                chat_id=update.message.chat.id, text=a_cat_lying_on_the_sand.escape(response['choices'][0]['message']['content']), parse_mode="MarkdownV2")
            data_list.append(
                {"role": "assistant", "content": response['choices'][0]['message']['content']})
            with open(history_text, 'w') as f:
                json.dump(data_list, f)

        print("LOG | GPT: Gpt over")


live_img_update_id = None


def stablediffusion(update, context):
    global live_img_update_id
    global fntext
    global fnnvtext
    global timmer
    global temp_var_delete
    global temp_var_edit_setting
    global user_id_list
    if a_cat_lying_on_the_sand.starupcheck() != 200:
        buttons = [[InlineKeyboardButton(
            "Click đây để nhắn cho master của tớ 🥺", url="https://t.me/rurimeiko")]]
        context.bot.sendMessage(reply_markup=InlineKeyboardMarkup(buttons), chat_id=update.message.chat.id,
                                text="Hiện tại server xử lý đồ hoạ đang offline rùi, cậu nhấn vào nút bên dưới để liên hệ mở lại server nhaaaa 🥺\nMaster của tớ thân thiện lắm nên cứ thoải mái trò chiện 😊")
    else:
        if update.message.chat.id not in user_id_list:
            user_id_list.append(update.message.chat.id)
            if len(user_id_list) <= 0:
                timmer = sec_timer
            print('LOG | STABLE DIFFUSION:',user_id_list)
        if len(user_id_list) > 0 and user_id_list[0] == update.message.chat.id:
            print(
                f'LOG | TELEGARM: User ({update.message.chat.username}) say {update.message.text}')
            timmer = sec_timer
            text = str(update.message.text).lower()
            if (text == "/draw") or (text == "/draw@randomfoodruribot"):
                buttons = [[InlineKeyboardButton(
                    "Cài đặt ⚙️", callback_data="settingdraw")]]
                temp_var_edit_setting = context.bot.sendMessage(reply_markup=InlineKeyboardMarkup(
                    buttons), chat_id=update.message.chat.id, text="Gõ `draw + chữ` để em vẽ hình cho nka 😶‍🌫️\nMẫu: `/draw thứ muốn xuất hiện trong ảnh \!\(thứ không muốn xuất hiện\)`", parse_mode="MarkdownV2")
            elif ("/draw" in text) or ("/draw@randomfoodruribot" in text):
                timmer = sec_timer
                live_img_update_id = update.message.chat.id
                text = text.replace(
                    "/draw ", "").replace("/draw@randomfoodruribot ", "")
                textprom = text.split("!(")
                if googletrans.Translator().detect(textprom[0]).lang == 'en':
                    fntext = textprom[0]
                else:
                    fntext = tran_vi_en.translate(textprom[0]).replace("&#39;",
                                                                "'").replace('&quot;', '"')
                fnnvtext = ""
                # a_cat_lying_on_the_sand.drawstb(fntext)
                if len(textprom) == 2:
                    if googletrans.Translator().detect(textprom[1]).lang == 'en':
                        fnnvtext = textprom[1]
                    else:
                        fnnvtext = tran_vi_en.translate(textprom[1]).replace("&#39;",
                                                                      "'").replace('&quot;', '"')
                    fnnvtext = fnnvtext.rstrip(")")

                buttons = [[InlineKeyboardButton("Square(512x512)", callback_data="drawaimagevippro1")], [InlineKeyboardButton(
                    "Landscape(800x400)", callback_data="drawaimagevippro2")], [InlineKeyboardButton("Portrait(400x800)", callback_data="drawaimagevippro3")]]
                a = context.bot.sendMessage(reply_markup=InlineKeyboardMarkup(buttons), chat_id=update.message.chat.id, text="<b>Cậu hãy bỏ qua tin nhắn này nếu không muốn tạo ảnh 🥺</b>\n<b>Prompt:</b> <code>" +
                                            fntext.replace("<", "&lt;").replace(">", "&gt;")+"</code>\n\n"+"<b>Negative prompt:</b> <code>"+fnnvtext.replace("<", "&lt;").replace(">", "&gt;")+"</code>", parse_mode="HTML")
                temp_var_delete = a
        else:
            context.bot.sendMessage(chat_id=update.message.chat.id, text="Cậu đang đứng thứ <b>" + str(user_id_list.index(update.message.chat_id) + 1) +
                                    "</b> trong hàng chờ cùng <span class='tg-spoiler'>" + str(random.randint(1000000000, 99999999999)) + "</span> người khác, ráng chờ lát nha 🤥🤭🤥", parse_mode="HTML")
            context.bot.send_sticker(
                chat_id=update.message.chat.id, sticker='CAACAgIAAxkBAAEfPB5kK-t41_kYFuqoEb1wOP7bJDTeVAACuj8AAuCjggcykMz6vc920i8E')


def get_image_live():
    global temp_var_delete_1
    global timmer
    while True:
        checkiss = True
        while isit:
            time.sleep(1)
            timmer = sec_timer
            if checkiss:
                a = context_bot.bot.sendMessage(chat_id=live_img_update_id, text=str(
                    round(float(a_cat_lying_on_the_sand.get_process())*100))+"%")
                temp_var_delete_1 = a
                checkiss = False
            else:
                try:
                    b = a_cat_lying_on_the_sand.get_process()
                    if float(b)*100 > 0:
                        context_bot.bot.editMessageText(
                            text=str(round(float(b)*100))+"%", chat_id=a.chat.id, message_id=a.message_id)

                except:
                    pass
        try:
            context_bot.bot.editMessageText(
                text="100"+"%", chat_id=a.chat.id, message_id=a.message_id)
        except:
            pass


def step_setting(update, context):
    if len(user_id_list) > 0 and user_id_list[0] == update.message.chat.id:
        global steps
        global timmer
        timmer = sec_timer
        if update.message.text == "/steps":
            update.message.reply_text(
                "Nhắn em `/steps + số` nhé \nVd như `/steps 20` 😎 \nCâu lưu ý thuộc tính này chỉ từ 1 tới 150 thôi nka 😊😊😊", parse_mode="MarkdownV2")
        else:
            steps = int(update.message.text.lower()[7:])
            if steps < 1:
                steps = 1
            elif steps > 150:
                steps = 150
            context.bot.sendMessage(
                chat_id=update.message.chat.id, text="Đã chỉnh steps thành: "+str(steps))

    else:
        context.bot.sendMessage(chat_id=update.message.chat.id,
                                text="Cậu chưa tham hàng chờ, hãy gõ <code>/draw</code> hoặc <code>/imgedit</code> để tham gia hàng chờ nhé🤥🤭🤥", parse_mode="HTML")
        context.bot.send_sticker(
            chat_id=update.message.chat_id, sticker='CAACAgIAAxkBAAEfPB5kK-t41_kYFuqoEb1wOP7bJDTeVAACuj8AAuCjggcykMz6vc920i8E')


def seed_setting(update, context):
    if len(user_id_list) > 0 and user_id_list[0] == update.message.chat.id:
        global seeds
        global timmer
        timmer = sec_timer

        if update.message.text == '/seeds':
            update.message.reply_text(
                "Nhắn em `/seeds + số` nhé \nVd như `/seeds 20` \nNhắn em `/seeds \-1` để random 🌱️🌱️🌱️", parse_mode="MarkdownV2")
        else:
            seeds = int(update.message.text.lower()[7:])
            context.bot.sendMessage(
                chat_id=update.message.chat.id, text="Đã chỉnh seeds thành: "+str(seeds))
    else:
        context.bot.sendMessage(chat_id=update.message.chat.id,
                                text="Cậu chưa tham hàng chờ, hãy gõ <code>/draw</code> hoặc <code>/imgedit</code> để tham gia hàng chờ nhé🤥🤭🤥", parse_mode="HTML")
        context.bot.send_sticker(
            chat_id=update.message.chat.id, sticker='CAACAgIAAxkBAAEfPB5kK-t41_kYFuqoEb1wOP7bJDTeVAACuj8AAuCjggcykMz6vc920i8E')


def cfg_setting(update, context):
    if len(user_id_list) > 0 and user_id_list[0] == update.message.chat.id:
        global cfg_scale
        global timmer
        timmer = sec_timer
        if update.message.text == '/cfg':
            update.message.reply_text(
                "Nhắn em `/cfg + số` nka \nVd như `/cfg 7` 🤭 \nCâu lưu ý thuộc tính này chỉ từ 1 tới 30 thôi nka 😊😊😊", parse_mode="MarkdownV2")
        else:
            cfg_scale = int(update.message.text.lower()[5:])
            if cfg_scale < 1:
                cfg_scale = 1
            elif cfg_scale > 30:
                cfg_scale = 30

            context.bot.sendMessage(
                chat_id=update.message.chat.id, text="Đã chỉnh cfg scale thành: "+str(cfg_scale))
    else:
        context.bot.sendMessage(chat_id=update.message.chat.id,
                                text="Cậu chưa tham hàng chờ, hãy gõ <code>/draw</code> hoặc <code>/imgedit</code> để tham gia hàng chờ nhé🤥🤭🤥", parse_mode="HTML")
        context.bot.send_sticker(
            chat_id=update.message.chat.id, sticker='CAACAgIAAxkBAAEfPB5kK-t41_kYFuqoEb1wOP7bJDTeVAACuj8AAuCjggcykMz6vc920i8E')


def gettext_imgedit(update, context):
    if a_cat_lying_on_the_sand.starupcheck() != 200:
        buttons = [[InlineKeyboardButton(
            "Click đây để nhắn cho master của tớ 🥺", url="https://t.me/rurimeiko")]]
        context.bot.sendMessage(reply_markup=InlineKeyboardMarkup(buttons), chat_id=update.message.chat.id,
                                text="Hiện tại server xử lý đồ hoạ đang offline rùi, cậu nhấn vào nút bên dưới để liên hệ mở lại server nhaaaa 🥺\nMaster của tớ thân thiện lắm nên cứ thoải mái trò chiện 😊")
    else:
        global timmer
        if update.message.chat.id not in user_id_list:
            user_id_list.append(update.message.chat.id)
            print('LOG | STABLE DIFFUSION:',user_id_list)
            if len(user_id_list) <= 0:
                timmer = sec_timer

        if len(user_id_list) > 0 and user_id_list[0] == update.message.chat.id:
            timmer = sec_timer
            update.message.reply_text(
                "Cậu hok gửi ảnh kìaaaa, tớ biết lấy ảnh ở đâu mà chạy lệnh này đâyyyyyy 🥹")
        else:
            context.bot.sendMessage(chat_id=update.message.chat.id, text="Cậu đang đứng thứ <b>" + str(user_id_list.index(update.message.chat_id) + 1) +
                                    "</b> trong hàng chờ cùng <span class='tg-spoiler'>" + str(random.randint(1000000000, 99999999999)) + "</span> người khác, ráng chờ lát nha 🤥🤭🤥", parse_mode="HTML")
            context.bot.send_sticker(
                chat_id=update.message.chat.id, sticker='CAACAgIAAxkBAAEfPB5kK-t41_kYFuqoEb1wOP7bJDTeVAACuj8AAuCjggcykMz6vc920i8E')


def handle_img_edit(update, context):
    if a_cat_lying_on_the_sand.starupcheck() != 200:
        buttons = [[InlineKeyboardButton(
            "Click đây để nhắn cho master của tớ 🥺", url="https://t.me/rurimeiko")]]
        context.bot.sendMessage(reply_markup=InlineKeyboardMarkup(buttons), chat_id=update.message.chat.id,
                                text="Hiện tại server xử lý đồ hoạ đang offline rùi, cậu nhấn vào nút bên dưới để liên hệ mở lại server nhaaaa 🥺\nMaster của tớ thân thiện lắm nên cứ thoải mái trò chiện 😊")
    else:
        global timmer
        if update.message.chat.id not in user_id_list:
            user_id_list.append(update.message.chat.id)
            print('LOG | STABLE DIFFUSION:',user_id_list)
            if len(user_id_list) <= 0:
                timmer = sec_timer

        if len(user_id_list) > 0 and user_id_list[0] == update.message.chat.id:
            buttons = None
            global fntext
            global fnnvtext
            timmer = sec_timer
            text = str(update.message.caption)
            a = context.bot.getFile(
                update["message"]["photo"][-1]["file_id"])['file_path']
            response = requests.get(a)
            link = os.path.join('stable_diffusion', str(uuid.uuid4())+".png")
            hasvariab = False
            if "/imgedit" in text.lower():
                if text.strip() != "/imgedit":
                    print('LOG | STABLE DIFFUSION INPUT PROMPT:',text)
                    fntext = ""
                    text = text.replace(
                        "/imgedit", "").replace("/imgedit@randomfoodruribot", "")
                    textprom = text.split("!(")
                    if googletrans.Translator().detect(textprom[0]).lang == 'en':
                        fntext = textprom[0]
                    else:
                        fntext = tran_vi_en.translate(textprom[0]).replace("&#39;",
                                                                    "'").replace('&quot;', '"')
                    fnnvtext = ""
                    # a_cat_lying_on_the_sand.drawstb(fntext)
                    if len(textprom) == 2:
                        if googletrans.Translator().detect(textprom[1]).lang == 'en':
                            fnnvtext = textprom[1]
                        else:
                            fnnvtext = tran_vi_en.translate(textprom[1]).replace("&#39;",
                                                                          "'").replace('&quot;', '"')
                        fnnvtext = fnnvtext.rstrip(")")

                    hasvariab = True
                if hasvariab and ((update["message"]["photo"][-1]["height"] > 1000) or (update["message"]["photo"][-1]["width"] > 1000)):
                    buttons = [[InlineKeyboardButton(
                        "Biến thể 😮", callback_data="1variable"+link[17:])]]
                elif ((update["message"]["photo"][-1]["height"] > 1000) or (update["message"]["photo"][-1]["width"] > 1000)) and (hasvariab == False):
                    context.bot.sendMessage(
                        chat_id=update.message.chat.id, text="Ảnhhh nì có kích thước lớn quá, tớ hok chịu nỗi, chức năng này chỉ hoạt động với ảnh dưới 1000px thui nha cậu 🥹\nNíu cậu mún lấy biến thể của ảnh nì thì nhớ thêm prompt render nhaaa 🤭")
                elif ((update["message"]["photo"][-1]["height"] < 1000) and (update["message"]["photo"][-1]["width"] < 1000)) and (hasvariab == False):
                    buttons = [[InlineKeyboardButton(
                                "Upscale 🤤", callback_data="upscale"+link[17:])]]
                else:
                    buttons = [[InlineKeyboardButton("Biến thể 😮", callback_data="1variable"+link[17:]), InlineKeyboardButton(
                                "Upscale 🤤", callback_data="upscale"+link[17:])]]
                if buttons != None:
                    with open(link, "wb") as f:
                        f.write(response.content)
                    context.bot.send_chat_action(
                        chat_id=user_id_list[0], action=ChatAction.UPLOAD_PHOTO)
                    context.bot.send_photo(reply_markup=InlineKeyboardMarkup(
                        buttons), caption="<b>Cậu hãy bỏ qua tin nhắn này nếu không muốn tạo ảnh 🥺</b>\n<b>Prompt:</b> <code>" +
                        fntext.replace("<", "&lt;").replace(">", "&gt;")+"</code>\n\n"+"<b>Negative prompt:</b> <code>"+fnnvtext.replace("<", "&lt;").replace(">", "&gt;")+"</code>", chat_id=update.message.chat.id, photo=open(link, 'rb'), parse_mode="HTML")

        else:
            context.bot.sendMessage(chat_id=update.message.chat.id, text="Cậu đang đứng thứ <b>" + str(user_id_list.index(update.message.chat_id) + 1) +
                                    "</b> trong hàng chờ cùng <span class='tg-spoiler'>" + str(random.randint(1000000000, 99999999999)) + "</span> người khác, ráng chờ lát nha 🤥🤭🤥", parse_mode="HTML")
            context.bot.send_sticker(
                chat_id=update.message.chat.id, sticker='CAACAgIAAxkBAAEfPB5kK-t41_kYFuqoEb1wOP7bJDTeVAACuj8AAuCjggcykMz6vc920i8E')


def bard_command(update, context):
    global bard_bot
    global re_bard
    history_text = "bard_chat/"+str(update.message.chat.id) + "_h.json"
    text = str(update.message.text).lower()

    if text == "/bard" or text == "/bard@randomfoodruribot":
        buttons = [[KeyboardButton("/bard clear")]]
        update.message.reply_text(reply_markup=ReplyKeyboardMarkup(
            buttons), text="Nhắn em `/bard + tin nhắn` để nhắn với tính cách gpt nhé 😊\nReset chat bằng `/bard clear` nhé ☺️", parse_mode="MarkdownV2")
    elif text == "/bard clear" or text == "/bard@randomfoodruribot clear":
        try:
            os.remove(history_text)
        except:
            print("LOG | BARD: Idk but cant clear log")
        context.bot.sendMessage(
            chat_id=update.message.chat.id, text="Đã xoá lịch sử chat với Bard 😊")
    else:
        text = str(update.message.text).lower()
        text = text.replace(
            "/bard ", "").replace("/bard@randomfoodruribot ", "")
        print('LOG | BARD INPUT:', text)

        if not os.path.isfile(history_text):
            with open(history_text, "w",  encoding="utf-8") as f:
                json.dump({'conversation_id': bard_bot.conversation_id,
                          'response_id': bard_bot.response_id, 'choice_id': bard_bot.choice_id}, f)

        else:
            print("LOG | BARD: Chat created")
        with open(history_text, 'r', encoding="utf-8") as json_file:
            history_chat = json.load(json_file)
        bard_bot.conversation_id = history_chat['conversation_id']
        bard_bot.response_id = history_chat['response_id']
        bard_bot.choice_id = history_chat['choice_id']
        re_bard = bard_bot.ask(text)
        buttons = []
        if 'last_mess_id' in history_chat:
            try:
                context.bot.editMessageText(message_id=str(history_chat['last_mess_id']), chat_id=update.message.chat.id, text=a_cat_lying_on_the_sand.escape(
                    history_chat['repon_mess']['content']), parse_mode="MarkdownV2")
            except:
                pass
        for i in range(len(re_bard['choices'])):
            if re_bard['choices'][i]['content'][0] == re_bard['content']:
                buttons.append(InlineKeyboardButton(
                    str(i+1)+' ⏺️', callback_data="bard_" + str(i)))
            else:
                buttons.append(InlineKeyboardButton(
                    str(i+1)+' ⬜', callback_data="bard_" + str(i)))
        if len(buttons) == 1:
            buttons = []
        id_emss = context.bot.sendMessage(reply_markup=InlineKeyboardMarkup([buttons]),
                                          chat_id=update.message.chat.id, text=a_cat_lying_on_the_sand.escape(re_bard['content']), parse_mode="MarkdownV2")
        with open(history_text, "w",  encoding="utf-8") as f:
            json.dump({'conversation_id': bard_bot.conversation_id, 'response_id': bard_bot.response_id,
                      'choice_id': bard_bot.choice_id, 'last_mess_id': id_emss.message_id, 'repon_mess': re_bard}, f)


def handle_voice_message(update, context):
    global Update_id
    print(
        f'LOG | TELEGARM: User ({update.message.chat.username}) send voice')
    Update_id = update.effective_message.chat_id
    link_voice = context.bot.getFile(
        update["message"]["voice"]["file_id"])['file_path']
    response = requests.get(link_voice)
    if int(update["message"]["voice"]["duration"]) > 18:
        update.message.reply_text(text="jztr 😳")
    with open(os.path.join('temp', 'user_voice.oga'), "wb") as f:
        f.write(response.content)
    # Load the Oga file
    ogg_file = AudioSegment.from_file(os.path.join('temp', "user_voice.oga"))
    # Convert the Ogg file to WAV format
    ogg_file.export(os.path.join('temp', 'user_voice.wav'), format="wav")

    header = {
        'Content-Type': 'audio/wav',
        'x-auth-token': '732d2e05-1524-4dae-a3af-6ccc3ba708a2',
        'x-device-id': '6AA5F258-5AAA-40CE-A301-140C583549B3',
        'x-user-id': '63b9abe1dde6bc422e7684e2'
    }
    with open(os.path.join('temp', 'user_voice.wav'), "rb") as file:
        wav_data = file.read()
    link_voice_uploaded = requests.post(
        'https://my.replika.com/api/mobile/1.5/voice_messages', headers=header, data=wav_data)
    send_message_replika(link_voice_uploaded.json()['voice_message_url'], if_voice=True, durian=float(
        update["message"]["voice"]["duration"]))


def runbot():
    global context_bot
    updater = Updater(credentials.bot_token, use_context=True)
    dp = updater.dispatcher
    context_bot = dp
    # Commands
    dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(CommandHandler('help', help_command))
    dp.add_handler(CommandHandler('random', random_command))
    dp.add_handler(CommandHandler('showlog', showlog_command))
    dp.add_handler(CommandHandler('addfood', addfood_command))
    dp.add_handler(CommandHandler('addsoup', addsoup_command))
    dp.add_handler(CommandHandler('showfood', showfood_command))
    dp.add_handler(CommandHandler('showsoup', showsoup_command))
    dp.add_handler(CommandHandler('getinfovps', getinfovps_command))
    dp.add_handler(CommandHandler('getsshurl', getsshurl_command))
    dp.add_handler(CommandHandler('spamsticker', spamsticker))
    dp.add_handler(CommandHandler('replika', handle_message))
    dp.add_handler(CommandHandler('tkb', tkb_command))
    dp.add_handler(CommandHandler('debug', debug_command))
    dp.add_handler(CommandHandler('null', null_command))
    dp.add_handler(CommandHandler('gpt', gpt_command))
    dp.add_handler(CommandHandler('bard', bard_command))
    dp.add_handler(CommandHandler('draw', stablediffusion))
    dp.add_handler(CommandHandler('steps', step_setting))
    dp.add_handler(CommandHandler('seeds', seed_setting))
    dp.add_handler(CommandHandler('cfg', cfg_setting))

    dp.add_handler(CommandHandler(command='imgedit', callback=gettext_imgedit))
    dp.add_handler(MessageHandler(Filters.photo, handle_img_edit))
    dp.add_handler(MessageHandler(Filters.voice, handle_voice_message))

    dp.add_handler(CallbackQueryHandler(callback_init))

    # Messages
    dp.add_handler(MessageHandler(Filters.text, handle_message))
    startup()

    # Log all errors
    dp.add_error_handler(error)

    # Run the bot
    updater.start_polling(1.0)


# Run the program
if __name__ == '__main__':
    t1 = threading.Thread(target=runbot)
    t2 = threading.Thread(target=get_message_replika)
    t3 = threading.Thread(target=gettkbovertime)
    t4 = threading.Thread(target=get_image_live)
    t1.start()
    t2.start()
    t3.start()
    t4.start()
