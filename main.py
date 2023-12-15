import requests
import json
import subprocess
from pyrogram import Client,filters
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import FloodWait
from pyromod import listen
from pyrogram.types import Message
import pyrogram
import tgcrypto
from p_bar import progress_bar
from details import api_id, api_hash, bot_token, sudo_groups
from urllib.parse import parse_qs, urlparse
from subprocess import getstatusoutput
import helper
import logging
import time
import aiohttp
import asyncio
import aiofiles
from aiohttp import ClientSession
from pyrogram.types import User, Message
import sys ,io
import re
import os
from pyrogram.types import InputMediaDocument
import time
import random 
from psutil import disk_usage, cpu_percent, swap_memory, cpu_count, virtual_memory, net_io_counters, boot_time
import asyncio
from pytube import Playlist
from pyrogram import Client, filters
from pyrogram.errors.exceptions import MessageIdInvalid
import os
from moviepy.editor import *
import yt_dlp
from bs4 import BeautifulSoup
from pyrogram.types import InputMediaDocument
from pyshorteners import Shortener

botStartTime = time.time()
batch = []
bot = Client(
    "bot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token)
      
@bot.on_message(filters.command(["start"]) & filters.chat(sudo_groups))
async def start_handler(bot: Client, m: Message):
    menu_text = (
        "Welcome to Meta Downloader Bot! \n\n"
        "[Generic Services]\n"
        "1. For All PDF /pdf\n"
        "2. For TXT /tor\n"
        "3. /cwdl \n" 
    )
    
    await m.reply_text(menu_text)


@bot.on_message(filters.command(["restart"]))
async def restart_handler(bot: Client, m: Message):
 rcredit = "Bot Restarted by " + f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
 if (f'{m.from_user.id}' in batch or batch == []) or m.from_user.id == sudo_groups:
    await m.reply_text("Restarted ✅", True)
    os.execl(sys.executable, sys.executable, *sys.argv)
 else:
 	await m.reply_text("You are not started this batch 😶.")

def meFormatter(milliseconds) -> str:
    milliseconds = int(milliseconds) * 1000
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        (f"{str(days)}d, " if days else "")
        + (f"{str(hours)}h, " if hours else "")
        + (f"{str(minutes)}m, " if minutes else "")
        + (f"{str(seconds)}s, " if seconds else "")
        + (f"{str(milliseconds)}ms, " if milliseconds else "")
    )
    return tmp[:-2]
  
def humanbytes(size):
    size = int(size)
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
    while size > power:
        size /= power
        n += 1
    return f"{str(round(size, 2))} {Dic_powerN[n]}B"

@bot.on_message(filters.command(["pdf"])&(filters.chat(sudo_groups)))
async def c_pdf(bot: Client, m: Message):
    editable = await m.reply_text("**Hello I am All in one pdf DL Bot\n\nSend TXT file To Download.**")
    input99: Message = await bot.listen(editable.chat.id)
    x = await input99.download()
    await input99.delete(True)
    try:         
        with open(x, "r", encoding="utf-8") as f:
             content = f.read()
             content = content.split("\n")
        links = []
        for i in content:
           if i != '':
                 links.append(i.split(":", 1))
        os.remove(x)
    except Exception as e:
        logging.error(e)
        await m.reply_text("Invalid file input ❌.")
        os.remove(x)
        return
        
    editable = await m.reply_text(f"Total links found in given txt {len(links)}\n\nSend From range, you want to download,\n\nInitial is 0")
    input1: Message = await bot.listen(editable.chat.id)
    count = input1.text
    count = int(count)      	
    	            
    await m.reply_text("**Enter Batch Name**")
    inputy: Message = await bot.listen(editable.chat.id)
    raw_texty = inputy.text        
    try:
        for i in range(count, len(links)):
          name = links[i][0]
          url = links[i][1]
          cc = f'{str(count).zfill(3)}. {name}.pdf\n\n**Batch:-** {raw_texty}\n\n'
          os.system(f'yt-dlp  "{url}" -N 200 -o "{name}.pdf"')
          await m.reply_document(f'{name}.pdf', caption=cc)
          count += 1
          os.remove(f'{name}.pdf')
          time.sleep(2)
    except Exception as e:
        await m.reply_text(e)
    await m.reply_text("Completed ✅")

@bot.on_message(filters.command(["stats"]))
async def stats(_,event: Message):
    logging.info('31')
    currentTime = meFormatter((time.time() - botStartTime))
    osUptime = meFormatter((time.time() - boot_time()))
    total, used, free, disk= disk_usage('/')
    total = humanbytes(total)
    used = humanbytes(used)
    free = humanbytes(free)
    sent = humanbytes(net_io_counters().bytes_sent)
    recv = humanbytes(net_io_counters().bytes_recv)
    cpuUsage = cpu_percent(interval=0.5)
    p_core = cpu_count(logical=False)
    t_core = cpu_count(logical=True)
    swap = swap_memory()
    swap_p = swap.percent
    swap_t = humanbytes(swap.total)
    memory = virtual_memory()
    mem_p = memory.percent
    mem_t = humanbytes(memory.total)
    mem_a = humanbytes(memory.available)
    mem_u = humanbytes(memory.used)
    stats = f'Bot Uptime: {currentTime}\n'\
            f'OS Uptime: {osUptime}\n'\
            f'Total Disk Space: {total}\n'\
            f'Used: {used} | Free: {free}\n'\
            f'Upload: {sent}\n'\
            f'Download: {recv}\n'\
            f'CPU: {cpuUsage}%\n'\
            f'RAM: {mem_p}%\n'\
            f'DISK: {disk}%\n'\
            f'Physical Cores: {p_core}\n'\
            f'Total Cores: {t_core}\n'\
            f'SWAP: {swap_t} | Used: {swap_p}%\n'\
            f'Memory Total: {mem_t}\n'\
            f'Memory Free: {mem_a}\n'\
            f'Memory Used: {mem_u}\n'
    
    await event.reply_text(f"{stats}")    


@bot.on_message(filters.command(["tor"])&(filters.chat(sudo_groups)))
async def txt_handler(bot: Client, m: Message):
    
    if batch != []:
        await m.reply("**⚠️ One Process Is Already Running**", quote=True)
        return
    else:
        batch.append(f'{m.from_user.id}')
        editable  = await m.reply_text("Send links listed in a txt file in format **Name:link**") 
    input0: Message = await bot.listen(editable.chat.id, filters.user(m.from_user.id))
    x = await input0.download()

    await input0.delete(True)
    file_name, ext = os.path.splitext(os.path.basename(x))
    credit = "Downloaded by " + f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
    try:         
        with open(x, "r") as f:
             content = f.read()
             content = content.split("\n")
        links = []
        for i in content:
           if i != '':
                 links.append(i)
        os.remove(x)
    except Exception as e:
        logging.error(e)
        await m.reply_text("Invalid file input ❌.")
        os.remove(x)
        return
    await editable.edit(f"Total links found are **{len(links)}**\n\nSend From where you want to download initial is **1**")
    input1: Message = await bot.listen(editable.chat.id, filters.user(m.from_user.id))
    raw_text = input1.text
    await input1.delete(True)
    
    await editable.edit("**Enter Batch Name or send `df` for grebbing it from txt.**")
    input0: Message = await bot.listen(editable.chat.id, filters.user(m.from_user.id))
    raw_text0 = input0.text 
    if raw_text0 == 'df':
        b_name = file_name
    else:
        b_name = raw_text0
    await input0.delete(True)  
    await editable.edit("**Enter resolution:**")
    input2: Message = await bot.listen(editable.chat.id, filters.user(m.from_user.id))
    raw_text22 = input2.text
    await input2.delete(True)
    try:
        if raw_text22 == "144":
            res = "256x144"
        elif raw_text22 == "240":
            res = "426x240"
        elif raw_text22 == "360":
            res = "640x360"
        elif raw_text22 == "480":
            res = "854x480"
        elif raw_text22 == "720":
            res = "1280x720"
        elif raw_text22 == "1080":
            res = "1920x1080" 
        else: 
            res = "UN"
    except Exception:
            res = "UN"
    await editable.edit("**Enter Caption or send `df` for default or just /skip**")    
    input7: Message = await bot.listen(editable.chat.id, filters.user(m.from_user.id))
    raw_text7 = input7.text 
    if raw_text7 == 'df':
        creditx = credit
    elif raw_text7 == '/skip':
        creditx = ''
    elif raw_text7 == '/skip@drmsupdlBot':
    	creditx = ''
    elif raw_text7 == '/skip@drmsupdlBot ':
    	creditx = ''
    else:
        creditx = raw_text7
    await input7.delete(True) 
    await editable.edit("Now send the **Thumb url**\nEg : `https://telegra.ph/file/15d338d5d116a1e591a10.jpg`\n\nor Send `no`")
    input6: Message = await bot.listen(editable.chat.id, filters.user(m.from_user.id))
    await input6.delete(True)
    await editable.delete()
    thumb = input6.text
    
    if thumb.startswith("http://") or thumb.startswith("https://"):
        getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"
    else:
        thumb == "no"
    if len(links) == 1:
        count = 1
    else:
        count = int(raw_text)   
    try:
        for i in range(count-1, len(links)):
            urlx = links[i].split('://', 1)[1].split(' ', 1)[0] if '://' in links[i] else 'nolinkfound'
            urly =  'https://'  + urlx if urlx != 'nolinkfound' else 'NoLinkFound'
            urlm = urly.replace('"', '').replace(',', '').replace('(','').replace(')','').strip()
            url = urly.replace('"', '').replace(',', '').replace('(','').replace(')','').replace("d1d34p8vz63oiq", "d26g5bnklkwsh4").replace("pw2.pc.cdn.bitgravity.com","d26g5bnklkwsh4.cloudfront.net").replace("file/d/","uc?export=download&id=").replace("www.youtube-nocookie.com/embed", "youtu.be").replace("?modestbranding=1", "").replace("/view?usp=sharing","").replace("d3nzo6itypaz07", "d26g5bnklkwsh4").replace("dn6x93wafba93", "d26g5bnklkwsh4").replace("d2tiz86clzieqa", "d26g5bnklkwsh4").replace("vod.teachx.in", "d3igdi2k1ohuql.cloudfront.net").replace("downloadappx.appx.co.in", "d33g7sdvsfd029.cloudfront.net").strip()
            parsed_url = urlparse(url)
            namex = links[i].strip().replace(urlm,'') if '://' in links[i].strip() and links[i].strip().replace(url,'') !='' else parsed_url.path.split('/')[-1]
            nameeex = namex if namex != '' and 'NoLinkFound' else 'NA'
            namme = nameeex.replace("\t", "").replace(":", "").replace("/","").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("/u","").replace('"','').replace('mp4','').replace('mkv','').replace('m3u8','').strip()[:60] + f"({res})" + ""
            name = namme.strip()
            if "videos.classplusapp" in url:
            	headers = {'Host': 'api.classplusapp.com', 'x-access-token': 'eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJpZCI6MzgzNjkyMTIsIm9yZ0lkIjoyNjA1LCJ0eXBlIjoxLCJtb2JpbGUiOiI5MTcwODI3NzQyODkiLCJuYW1lIjoiQWNlIiwiZW1haWwiOm51bGwsImlzRmlyc3RMb2dpbiI6dHJ1ZSwiZGVmYXVsdExhbmd1YWdlIjpudWxsLCJjb3VudHJ5Q29kZSI6IklOIiwiaXNJbnRlcm5hdGlvbmFsIjowLCJpYXQiOjE2NDMyODE4NzcsImV4cCI6MTY0Mzg4NjY3N30.hM33P2ai6ivdzxPPfm01LAd4JWv-vnrSxGXqvCirCSpUfhhofpeqyeHPxtstXwe0', 'user-agent': 'Mobile-Android', 'app-version': '1.4.37.1', 'api-version': '18', 'device-id': '5d0d17ac8b3c9f51', 'device-details': '2848b866799971ca_2848b8667a33216c_SDK-30', 'accept-encoding': 'gzip'}
            	params = (('url', f'{url}'),)
            	response = requests.get('https://api.classplusapp.com/cams/uploader/video/jw-signed-url', headers=headers, params=params)
            	url = response.json()['url']
            elif "visionias" in url:
                async with ClientSession() as session:
                    async with session.get(url, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Pragma': 'no-cache', 'Referer': 'http://www.visionias.in/', 'Sec-Fetch-Dest': 'iframe', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'cross-site', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Linux; Android 12; RMX2121) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36', 'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"', 'sec-ch-ua-mobile': '?1', 'sec-ch-ua-platform': '"Android"',}) as resp:
                        text = await resp.text()
                        url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)
            elif "d26g5bnklkwsh4" in url:
            	vida = url.split("/")[-2]
            	url = f"https://d26g5bnklkwsh4.cloudfront.net/{vida}/master.m3u8"
            elif "nocookie.com" in url:
                url = url.replace('-nocookie', '')
            elif "d9an9suwcevit" in url:

            	 urlx = url.replace("master.m3u8", "master_tunak_tunak_tun.m3u8")

            	 response = requests.get(urlx)

            	 if response.status_code != 200:

            	 	url = url.replace("master_tunak_tunak_tun.m3u8", "master.m3u8")

            	 else:

            	 	url = urlx
            elif ".pdf" in url:
                cmd = "pdf"
            if "youtu" in url:
                ytf = f"b[height<={raw_text22}][ext=mp4]/bv[height<={raw_text22}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
            else:
                ytf = f"b[height<={raw_text22}]/bv[height<={raw_text22}]+ba/b/bv+ba"
            if "jw-prod" in url:
                cmd = f'yt-dlp -o "{name}.mp4" "{url}"'
            else:
                cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'               
            try:
                Show = f"**Trying To Download:-**\n\n**Name :-** `{name}`\n**Quality :-** `{res}`\n\n**Piracy is illegal 🚫**\n"
                prog = await m.reply_text(Show)
                cc = f'**Index  » **{str(count).zfill(3)}\n**Title » **{name}.mkv\n**Batch: **{b_name}\n\n**{creditx}**'
                if cmd == "pdf" in url or ".pdf"  in url or "drive"  in url:
                    try:
                        ka=await helper.aio(url,name)
                        await prog.delete (True)
                        time.sleep(1)
                        reply = await m.reply_text(f"Trying To Upload - `{name}`")
                        time.sleep(1)
                        copy = await bot.send_document(chat_id = m.chat.id, document = ka, caption=f'**Index  » ** {str(count).zfill(3)}\n**Title » ** {name}.pdf\n**Batch: ** {b_name}\n\n{creditx}')
                        count+=1
                        await reply.delete (True)
                        time.sleep(10)
                        os.remove(ka)
                        time.sleep(3)
                    except FloodWait as e:
                        logging.error(e)
                        await m.reply_text(str(e))
                        time.sleep(e.x+1)
                        continue
                else:
                    res_file = await helper.download_video(url,cmd, name)
                    filename = res_file
                    await helper.send_vid(bot, m,cc,filename,thumb,name,prog)
                    count+=1
                    time.sleep(1)
            except Exception as e:
                logging.error(e)
                await m.reply_text(f"**Failed To Download ❌**\n**Name** - {name}\n**Link** - `{urlm}`")
                if "NoLinkFound" != url:
                 count+=1
                time.sleep(20)
                continue
    except Exception as e:
        logging.error(e)
        await m.reply_text(e)
        
    await m.reply_text("Done ✅")
    
    batch.clear() 
    
@bot.on_message(filters.command(["cdwl"]))
async def start(bot, update):
       await update.reply_text("Hi i am **Careerwill Downloader**.\n\n"
                              "**NOW:-** "
                                       
                                       "Press **/login** to continue..\n\n")
                                     

ACCOUNT_ID = "6206459123001"
BCOV_POLICY = "BCpkADawqM1474MvKwYlMRZNBPoqkJY-UWm7zE1U769d5r5kqTjG0v8L-THXuVZtdIQJpfMPB37L_VJQxTKeNeLO2Eac_yMywEgyV9GjFDQ2LTiT4FEiHhKAUvdbx9ku6fGnQKSMB8J5uIDd"
bc_url = (
    f"https://edge.api.brightcove.com/playback/v1/accounts/{ACCOUNT_ID}/videos"
)
bc_hdr = {"BCOV-POLICY": BCOV_POLICY}

url="https://elearn.crwilladmin.com/api/v1/"

info= {
 "deviceType":"android",
    "password":"",
    "deviceModel":"Asus ASUS_X00TD",
    "deviceVersion":"Pie(Android 9.0)",
    "email":"",
}

@bot.on_message(filters.command(["login"]))
async def account_login(bot: Client, m: Message):
    editable = await m.reply_text(
        "Send **ID & Password** in this manner otherwise bot will not respond.\n\nSend like this:-  **ID*Password**"
    )

    input1: Message = await bot.listen(editable.chat.id)
    raw_text = input1.text
    info["email"] = raw_text.split("*")[0]
    info["password"] = raw_text.split("*")[1]
    await input1.delete(True)

    login_response=requests.post(url+"login-other",info)
    token=login_response.json( )["data"]["token"]
    await editable.edit("**login Successful**")
    await editable.edit("You have these Batches :-")
    
    url1 = requests.get("https://elearn.crwilladmin.com/api/v1/comp/my-batch?&token="+token)
    b_data = url1.json()['data']['batchData']

    cool=""
    for data in b_data:
        aa=f"**Batch Name -** {data['batchName']}\n**Batch ID -** ```{data['id']}```\n**By -** {data['instructorName']}\n\n"
        if len(f'{cool}{aa}')>4096:
            await m.reply_text(aa)
            cool =""
        cool+=aa
    await m.reply(cool)

    editable1= await m.reply_text("**Now send the Batch ID to Download**")
    input2 = message = await bot.listen(editable.chat.id)
    raw_text2 = input2.text

# topic id url = https://elearn.crwilladmin.com/api/v1/comp/batch-topic/881?type=class&token=d76fce74c161a264cf66b972fd0bc820992fe576
    url2 = requests.get("https://elearn.crwilladmin.com/api/v1/comp/batch-topic/"+raw_text2+"?type=class&token="+token)
    topicid = url2.json()["data"]["batch_topic"]
    bn =url2.json()["data"]["batch_detail"]["name"]
    await m.reply_text(f'Batch details of **{bn}** are :')
    cool1 = ""
    for data in topicid:
        t_name=(data["topicName"])
        tid = (data["id"])
        
        urlx = "https://elearn.crwilladmin.com/api/v1/comp/batch-detail/"+raw_text2+"?redirectBy=mybatch&topicId="+tid+"&token="+token
        ffx = requests.get(urlx)
        vcx =ffx.json()["data"]["class_list"]["batchDescription"]
        vvx =ffx.json()["data"]["class_list"]["classes"]
        vvx.reverse()
        zz= len(vvx)
        
       
        hh = f"**Topic -** {t_name}\n**Topic ID - ** ```{tid}```\nno. of videos are : {zz}\n\n"
        
        if len(f'{cool1}{hh}')>4096:
            await m.reply_text(hh)
            cool1=""
        cool1+=hh
    await m.reply_text(cool1)
    await m.reply_text(f'**{vcx}**')

    editable2= await m.reply_text("**Now send the Topic ID to Download**")
    input3 = message = await bot.listen(editable.chat.id)
    raw_text3 = input3.text
    
    editable3= await m.reply_text("**Now send the Resolution**")
    input4 = message = await bot.listen(editable.chat.id)
    raw_text4 = input4.text

    # editable4= await m.reply_text("Now send the **Thumb url** or send **no**")
    # input6 = message = await bot.listen(editable.chat.id)
    # raw_text6 = input6.text

    # thumb = input6.text
    # if thumb.startswith("http://") or thumb.startswith("https://"):
    #     getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
    #     thumb = "thumb.jpg"
    # else:
    #     thumb == "no"

    
    
    #gettting all json with diffrent topic id https://elearn.crwilladmin.com/api/v1/comp/batch-detail/881?redirectBy=mybatch&topicId=2324&token=d76fce74c161a264cf66b972fd0bc820992fe57
    
    url3 = "https://elearn.crwilladmin.com/api/v1/comp/batch-detail/"+raw_text2+"?redirectBy=mybatch&topicId="+raw_text3+"&token="+token   
    ff = requests.get(url3)
    #vc =ff.json()["data"]["class_list"]["batchDescription"]
    mm = ff.json()["data"]["class_list"]["batchName"]
    
    vv =ff.json()["data"]["class_list"]["classes"]
    vv.reverse()
    #clan =f"**{vc}**\n\nNo of links found in topic-id {raw_text3} are **{len(vv)}**"
    #await m.reply_text(clan)
    count = 1
    try:
        for data in vv:
            vidid = (data["id"])
            lessonName = (data["lessonName"]) 
            bcvid = (data["lessonUrl"][0]["link"])
            
        
            if bcvid.startswith("62"):
                try:
                    video_response = requests.get(f"{bc_url}/{bcvid}", headers=bc_hdr)
                    video = video_response.json()
                    video_source = video["sources"][5]
                    video_url = video_source["src"]
                    #print(video_url)

                    surl=requests.get("https://elearn.crwilladmin.com/api/v1/livestreamToken?type=brightcove&vid="+vidid+"&token="+token)
                    stoken = surl.json()["data"]["token"]
                    #print(stoken)

                    link = video_url+"&bcov_auth="+stoken
                    #print(link)
                except Exception as e:
                    print(str(e))
                
            else:
                link="https://www.youtube.com/embed/"+bcvid
            # await m.reply_text(link)

            #editable3= await m.reply_text("**Now send the Resolution**")
            #input4 = message = await bot.listen(editable.chat.id)
            #raw_text4 = input4.text

            cc = f"**{count}) Title :** {lessonName}\n\n**Quality :** {raw_text4}\n**Batch :** {mm}\n\n**THESE VIDEOS ARE NOT FOR SELLING PURPOSE**"
            Show = f"**Downloading:-**\n```{lessonName}\nQuality - {raw_text4}```\n\n**Url :-** ```{link}```"
            prog = await m.reply_text(Show)

            if "youtu" in link:
                if raw_text4 in ["144", "240", "480"]:
                    ytf = f"'bestvideo[height<={raw_text4}][ext=mp4]+bestaudio[ext=m4a]'"
                elif raw_text4 == "360":
                    ytf = 18
                elif raw_text4 == "720":
                    ytf = 22
                else:
                    ytf = 18
            else:
                ytf=f"bestvideo[height<={raw_text4}]"

            try:
                
                
                cmd = f'yt-dlp -o "{lessonName}.mp4" -f "{ytf}+bestaudio" "{link}"'
                download_cmd = f"{cmd} -R 25 --fragment-retries 25 --external-downloader aria2c --downloader-args 'aria2c: -x 16 -j 32'"
                os.system(download_cmd)
            

                filename = f"{lessonName}.mp4"
                subprocess.run(f'ffmpeg -i "{filename}" -ss 00:00:19 -vframes 1 "{filename}.jpg"', shell=True)
                
                
                # thumbnail = f"{filename}.jpg"
                try:
                    if thumb == "":
                        thumbnail = f"{filename}.jpg"
                    else:
                        thumbnail = thumb
                except Exception as e:
                    print(e)



                dur = int(helper.duration(filename))

                await m.reply_video(f"{lessonName}.mp4",caption=cc, supports_streaming=True,height=720,width=1280,thumb=thumbnail,duration=dur)
                count +=1
                os.remove(f"{lessonName}.mp4")
                await prog.delete (True)
                os.remove(f"{filename}.jpg")
            except Exception:
                continue

    except Exception as e:
        await m.reply_text(str(e))
    await m.reply_text("Done")


bot.run()
