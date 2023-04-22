import os
import requests
import io
import base64
import uuid
import json
#bm bị ngu
from PIL import Image, PngImagePlugin


url = None

def reloadlink():
    global url
    with open('credentials-user.json', 'r') as file:
    # Load the data from the file
        data = json.load(file)
    url = data['url']+"/"
    print (url)
session = requests.Session()
reloadlink()
def starupcheck():
    try:
        a = session.get(timeout=5,url=url + 'startup-events')
    except:
        return(False)
    return a.status_code

def start():
    option_payload = {
            'live_previews_enable': False
        }
    try:
        a = session.post(timeout=5, url=url + 'sdapi/v1/options', json = option_payload)
    except:
        return(False)
    return a.status_code

def getinfoimage(link):
    targetImage = Image.open(link)
    s = targetImage.text
    a  = s['parameters']
    a = a.split("\n")
    b= a[-1].split(",")
    a.pop(-1)
    a.extend(b)
    my_list = a
    my_dict = {}
    for index, item in enumerate(my_list):
        if index == 0:
            key = "Prompt"
            value = item.strip()
        else:
            key, value = item.split(": ")
        my_dict[key.strip()] = value.strip()
    json_data = json.dumps(my_dict)
    return json_data

# a_cat_lying_on_the_sand.py:
def get_all_sampler():
    response4 = session.get(url= url+'sdapi/v1/samplers')
    allsampler = response4.json()
    listtemp =[]
    for i in range(len(allsampler)):
        listtemp.append(allsampler[i]['name'])
    return listtemp


def drawstb(textpromt,promtnga,step,sample,seeds, cfg_scale, width, height):
    payload = {
        "prompt": textpromt,
        "negative_prompt":promtnga,
        "sampler_name": sample,
        "steps": step,
        "seed": seeds,
        "cfg_scale": cfg_scale,
        "width": width,
        "height": height
    }
    response = session.post(url= url +'sdapi/v1/txt2img', json=payload).json()
    for i in response['images']:
        image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))
        png_payload = {
            "image": "data:image/png;base64," + i
        }
        response2 = session.post(url=f'{url}sdapi/v1/png-info', json=png_payload)
        pnginfo = PngImagePlugin.PngInfo()
        pnginfo.add_text("parameters", response2.json().get("info"))
        link = os.path.join('stable_diffusion', str(uuid.uuid4())+".png")
        image.save(link, pnginfo=pnginfo)

    return link

def img2img(img_path, textpromt, promtnga, step, sample,seeds, cfg_scale, width, height):
    with open(img_path, "rb") as image_file:
        data = base64.b64encode(image_file.read()).decode('utf-8')
    payload = {
        "init_images": [data],
        "prompt": textpromt,
        "negative_prompt":promtnga,
        "sampler_name": sample,
        "steps": step,
        "seed": seeds,
        "cfg_scale": cfg_scale,
        "width": width,
        "height": height
    }

    response = session.post(url= url +'sdapi/v1/img2img', json=payload).json()

    for i in response['images']:
        image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))
        png_payload = {
            "image": "data:image/png;base64," + i
        }
        response2 = session.post(url=f'{url}sdapi/v1/png-info', json=png_payload)
        pnginfo = PngImagePlugin.PngInfo()
        pnginfo.add_text("parameters", response2.json().get("info"))
        link = os.path.join('stable_diffusion', str(uuid.uuid4())+".png")
        image.save(link, pnginfo=pnginfo)


    return link




def set_model(name):
    option_payload = {
        "sd_model_checkpoint": name
    }
    a = session.post(url=url + 'sdapi/v1/options', json = option_payload)
    return a.status_code == 200

def get_all_model(type='model_name'):
    response4 = session.get(url= url+'sdapi/v1/sd-models')
    allmodel = response4.json()
    listemp =[]
    for i in range(len(allmodel)):
        listemp.append(allmodel[i][type])
    return listemp

def get_model():
    response4 = session.get(url= url+'sdapi/v1/options')
    return response4.json()['sd_model_checkpoint']

def get_process(): 
    head = {'accept': 'application/json'}
    try:
        response4 = session.get(url= url+'sdapi/v1/progress?skip_current_image=true',headers=head)
    except: pass
    response4 = response4.json()
    return response4['progress']

def upscale_img(upscaler1, upscaler2, img_path):
    with open(img_path, "rb") as image_file:
        data = base64.b64encode(image_file.read()).decode('utf-8')
    
    payload = {
        "upscaler_1": upscaler1,
        "upscaler_2": upscaler2,
        "image": data
    }
    response = session.post(url= url +'sdapi/v1/extra-single-image', json=payload).json()
    image = Image.open(io.BytesIO(base64.b64decode(response['image'].split(",",1)[0])))
    png_payload = {
        "image": "data:image/png;base64," + response['image']
    }
    response2 = session.post(url=f'{url}sdapi/v1/png-info', json=png_payload)
    pnginfo = PngImagePlugin.PngInfo()
    pnginfo.add_text("parameters", response2.json().get("info"))
    link = os.path.join('stable_diffusion', str(uuid.uuid4())+".png")
    image.save(link, pnginfo=pnginfo)
    return link


def get_all_upscaler():
    response = session.get(url= url+'sdapi/v1/upscalers')
    all_upscalers = response.json()
    listtemp =[]
    for i in range(len(all_upscalers)):
        if all_upscalers[i]['name'] != "LDSR":
            listtemp.append(all_upscalers[i]['name'])
    return listtemp


def escape(s:str) -> str:
    list = '_', '*', '[', ']', '(', ')', '~', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!','`'
    s = s.replace('```','\code\\')
    for i in list:
        s = s.replace(i,"\\"+i)
    s = s.replace('\code\\','```')
    return s
