# thg nao doc dc nhan su phu day magic
# who could read this code is my master of magic
# bonus hint background music https://youtu.be/pIrOAyXIjak
import json
import re
from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta

import requests
magic_var = True
magic2_var = True
checktkbisupdate = True
html = ''
cookie = None
mana_point = 1
def magic3(t, start, end): 
    if (t > start and t < end) :
        return True
    return False
def reloadcookie():
    global cookie
    with open('credentials-user.json', 'r') as file:
    # Load the data from the file
        data = json.load(file)
    cookie = {'ASC.AUTH': data['ASC.AUTH']}
reloadcookie()
def magic4():
    global magic_var
    global magic2_var
    global checktkbisupdate
    global html
    if magic3(datetime.strptime("19:00:00",  "%H:%M:%S") - datetime.strptime(datetime.now().strftime("%H:%M:%S"), "%H:%M:%S"), timedelta(hours = 0), timedelta(hours = 1)):
        magic2_var = True
    if magic_var or (magic2_var and magic3(datetime.strptime(datetime.now().strftime("%H:%M:%S"), "%H:%M:%S")-datetime.strptime("00:00:00", "%H:%M:%S"), timedelta(hours = 0), timedelta(hours = 1))):
        # Create the soup object
        magic_var = False
        magic2_var = False
        header = {
            'authority': 'sinhvien.ctuet.edu.vn',
            'method': 'POST',
            'path': '/SinhVien/GetDanhSachLichTheoTuan',
            'scheme': 'https',
            'accept': 'text/html, */*; q=0.01',
            'origin': 'https://sinhvien.ctuet.edu.vn',
            'referer': 'https://sinhvien.ctuet.edu.vn/lich-theo-tuan.html'
        }
        print('LOG | LEASSON ALLERT:',cookie)
             # 0 = tất cả, 1 = lịch học, 2 = lịch thi
        payload = {'pNgayHienTai': date.today().strftime("%d/%m/%Y"), 'pLoaiLich': 1}
        url = 'https://sinhvien.ctuet.edu.vn/SinhVien/GetDanhSachLichTheoTuan'
        x = requests.post(url, headers=header, cookies=cookie, json=payload)
        html = x.text
        checktkbisupdate = True
    return html

dmtime = {
1:['7::00::00', '7::50::00', '00::00::00'],
2:['7::50::00', '8::40::00', '00::15::00'],
3:['8::55::00', '9::45::00', '00::00::00'],
4:['9::45::00', '10::35::00', '00::05::00'],
5:['10::40::00', '11::30::00', '00::00::00'],
6:['13::20::00', '14::10::00', '00::00::00'],
7:['14::10::00', '15::00::00', '00::15::00'],
8:['15::15::00', '16::05::00', '00::00::00'],
9:['16::05::00', '16::55::00', '00::05::00'],
10:['17::00::00', '17::50::00', '00::00::00'],
11:['18::20::00', '19::10::00', '00::00::00'],
12:['19::10::00', '20::00::00', '00::05::00'],
13:['20::05::00', '20::55::00', '00::00::00']
}


def gettimeinout(s):
    tiet = re.findall(r'\d+', s)
    break_times= []
    in_time = datetime.strptime(dmtime[int(tiet[0])][0], '%H::%M::%S').time()
    
    for i in range(int(tiet[0]),int(tiet[1])):
        out_time  = datetime.strptime(dmtime[i][1], '%H::%M::%S').time()
        if dmtime[i][2] != '00::00::00':
            break_time  = datetime.strptime(dmtime[i][2], '%H::%M::%S').time()
            break_times.append("Nghỉ "+break_time.strftime("%M phút")+" vào lúc "+out_time.strftime("%I:%M %p"))
    out_time  = datetime.strptime(dmtime[int(tiet[1])][1], '%H::%M::%S').time()

    return [in_time.strftime("%I:%M %p"),out_time.strftime("%I:%M %p"),break_times]


def tack_subject(array):
    result = []
    for i in range(len(array)):
        if array[i][:2] == "GV":
            array.pop(i)
            array.append('null')
    
    array= list(filter(lambda a: a != "null", array))
    for i in range(0, len(array), 4):
        result.append([
            array[i],
            array[i + 1],
            gettimeinout(array[i + 2]),
            array[i + 3],
        ])
    return result
tkb_before = None
def magic():
    global checktkbisupdate
    global tkb_before
    magic4()
    if (checktkbisupdate):
        checktkbisupdate = False
        soup = BeautifulSoup(html, 'html.parser') 
        morning = []
        afternoon = []
        evening = []
        dates = []

        time = 0

        # Find all elements with a role attribute
        for div in soup.find_all(attrs={"role": True}):
            if div['role'] == "row":
                for e in div:
                    if e.text == 'Sáng':
                        time = 1
                        continue
                    elif e.text == 'Chiều':
                        time = 2
                        continue
                    elif e.text == 'Tối':
                        time = 3
                        continue
                    elif e.text == 'Ca học':
                        time = 4
                        continue
                    elif e.text == '\n':
                        continue 
                    
                    if time == 1:
                            morning.append(e.text)
                    elif time == 2:
                            afternoon.append(e.text)
                    elif time == 3:
                            evening.append(e.text)
                    elif time == 4:
                            dates.append(e.text)


        tkb = []

        for i in range(7):
            pattern = {}
            m = morning[i].replace('\n\n', '').split('\n')
            a = afternoon[i].replace('\n\n', '').split('\n')
            e = evening[i].replace('\n\n', '').split('\n')

            if i == 6:
                pattern['day'] = dates[i][:8]
                pattern['date'] =  dates[i][8:]
            else:
                pattern['day'] = dates[i][:5]
                pattern['date'] =  dates[i][5:]

            if len(m) > 1:
                pattern['morning'] = tack_subject(m) 
            else:
                pattern['morning'] = ['null']

            if len(a) > 1:
                pattern['afternoon'] = tack_subject(a) 
            else:
                pattern['afternoon'] = ['null']

            if len(e) > 1:
                pattern['evening'] = tack_subject(e) 
            else:
                pattern['evening'] = ['null']

            tkb.append(pattern)
        print("LOG | LEASSON ALLERT: ĐÃ CẬP NHẬT TKB THÀNH CÔNG!")
        tkb_before = tkb
        return tkb
    else: return tkb_before
def magic2():
    t = datetime.now()
    dict = magic()[t.weekday()]
    if datetime.strptime(t.strftime("%H:%M:%S"), "%H:%M:%S") < datetime.strptime('11:00:00', "%H:%M:%S"):
        for i in range(0, len(dict['morning'])):
            lesson = dict['morning'][i]
            if lesson == 'null':
                return '\!\!del learn\!\! ze zeeeee\!\!\!\!\!'
            if magic3(datetime.strptime(lesson[2][0], "%I:%M %p") - datetime.strptime(t.strftime("%H:%M:%S"), "%H:%M:%S"), timedelta(hours = 0), timedelta(hours = mana_point)):
                return "*" + lesson[0] + "*" + '\n' + lesson[1].replace("-","\-") + '\n' + '`' + lesson[2][0] + '`'  + '\n' + '`' + lesson[2][1] + '`' + '\n' + '; '.join(lesson[2][2]) + '\n' + lesson[3]

    elif datetime.strptime(t.strftime("%H:%M:%S"), "%H:%M:%S") < datetime.strptime('17:00:00', "%H:%M:%S"):
        for i in range(0, len(dict['afternoon'])):
            lesson = dict['afternoon'][i]
            if lesson == 'null':
                return '\!\!del learn\!\! ze zeeeee\!\!\!\!\!'
            if magic3(datetime.strptime(lesson[2][0], "%I:%M %p") - datetime.strptime(t.strftime("%H:%M:%S"), "%H:%M:%S"), timedelta(hours = 0), timedelta(hours = mana_point)):
                return "*" + lesson[0] + "*" + '\n' + lesson[1].replace("-","\-") + '\n' + '`' + lesson[2][0] + '`'  + '\n' + '`' + lesson[2][1] + '`' + '\n' + '; '.join(lesson[2][2]) + '\n' + lesson[3]
    else:
        for i in range(0, len(dict['evening'])):
            lesson = dict['evening'][i]
            if lesson == 'null':
                return '\!\!del learn\!\! ze zeeeee\!\!\!\!\!'
            if magic3(datetime.strptime(lesson[2][0], "%I:%M %p") - datetime.strptime(t.strftime("%H:%M:%S"), "%H:%M:%S"), timedelta(hours = 0), timedelta(hours = mana_point)):
                return "*" + lesson[0] + "*" + '\n' + lesson[1].replace("-","\-") + '\n' + '`' + lesson[2][0] + '`'  + '\n' + '`' + lesson[2][1] + '`' + '\n' + '; '.join(lesson[2][2]) + '\n' + lesson[3]
    



def magic6(dict, noon):
    for i in range(0, len(dict[noon])):
        lesson = dict[noon][i]
        if lesson == 'null':
            return '\!\!del learn\!\! ze zeeeee\!\!\!\!\!'
        else:
            return "*" + lesson[0] + "*" + '\n' + lesson[1].replace("-","\-") + '\n' + '`' + lesson[2][0] + '`'  + '\n' + '`' + lesson[2][1] + '`' + '\n' + '; '.join(lesson[2][2]) + '\n' + lesson[3]

def magic5(i):
    if (magic6(magic()[i], 'morning') == '\!\!del learn\!\! ze zeeeee\!\!\!\!\!') and (magic6(magic()[i], 'afternoon') == '\!\!del learn\!\! ze zeeeee\!\!\!\!\!') and (magic6(magic()[i], 'evening') == '\!\!del learn\!\! ze zeeeee\!\!\!\!\!'):
        return ""
    return magic()[i]['day'] + ', ' + magic()[i]['date'] + '\n' + '*MORNING:*' + '\n' + magic6(magic()[i], 'morning') + '\n' + '*AFTERNOON:*' + '\n' + magic6(magic()[i], 'afternoon') + '\n' + '*EVENING:*' + '\n' + magic6(magic()[i], 'evening')
