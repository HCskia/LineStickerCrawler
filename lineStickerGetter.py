import concurrent
import json
import os

import aiohttp
import asyncio

import requests
from bs4 import BeautifulSoup


def writeLog(context):
    print(context)
    with open("log.txt", 'a', encoding="utf-8")as f:
        f.write(context)
        f.close()

def getProxy():
    Proxy = "0"
    with open("config.json", 'r+', encoding="utf-8")as f:
        Proxy = json.loads(f.read())['proxy']
        f.close()
    writeLog(f"Get Proxy：{Proxy}\n")
    return Proxy

def lineStickerGetter():
    head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
    proxy = {'https':f"http://127.0.0.1:{getProxy()}",'http':f"http://127.0.0.1:{getProxy()}"}
    url = input("请输入贴纸ID：")
    try:
        resp = requests.get(url=f"https://store.line.me/stickershop/product/{url}/zh-Hans", proxies=proxy, headers=head)
        soup = BeautifulSoup(resp.content, 'html.parser')
    except concurrent.futures._base.TimeoutError:
        writeLog("connection time out\n")
        return 0
    except aiohttp.client_exceptions.ClientConnectorError:
        writeLog("connection ERROR,maybe Proxy ERROR\n")
        return 0
    except Exception as e:
        writeLog(f"Unknow ERROR：{e}\n")
        return 0
    title = soup.find("title").get_text().replace(" – LINE stickers | LINE STORE","").replace('"',"").replace("."," ").replace(":"," ")
    writeLog(f"Get Title:{title}")
    soup = soup.find("div", attrs={'class': 'mdCMN09ImgListWarp'})
    try:
        os.makedirs(f"out/{title}")
        writeLog(f"make title dir Success!")
    except Exception as e:
        writeLog(f"EROOR! make title dir Filed! {e}")
        return 0

    stickersUrl = []
    for temp in soup.find_all("li"):
        temp = str(temp)
        temp = temp[temp.find("'{")+2:temp.find("}'")]
        temp = '{' + temp + '}'
        temp = json.loads(temp)
        temp = temp['staticUrl']
        stickersUrl.append(temp)

    Count = 0
    for temp in stickersUrl:
        writeLog(f"DownLoadStickers From {temp}\n")
        StickerDownload = requests.get(url=temp,proxies=proxy)
        with open(rf"out\{title}\sticker-{Count}.png", 'wb+') as f:
            f.write(StickerDownload.content)
            f.close()
        Count += 1
    #print(soup)

lineStickerGetter()