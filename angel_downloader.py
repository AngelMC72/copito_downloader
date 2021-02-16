"""
Angel_Downloader_v1.0

Descarga todos los videos a partir de un csv.
Los videos se ubicarán en la misma carpeta donde se ejecute este script.
Optional: Create folders for the files.
"""

import urllib, json 
import requests
from bs4 import BeautifulSoup
import io
import os
import glob
import shutil
import re
from csv import DictReader
import time
import ffmpeg

## Abre "paste_here.csv" y pega los links en la columna "id"
with open("paste_here.csv") as f:
    long_links = [row["id"] for row in DictReader(f)]

codes =[]
for ll in long_links:
    code = re.findall(r'wvideo=(.*?)"', ll)
    codes.append(code[0])
#print(codes)

video_names = []
bin_links = []
json_links =[]
video_namecheck =[]

for code in codes:
    ts_rem = "https://fast.wistia.com/embed/medias/"+str(code)+".json"
    json_links.append(ts_rem)
#print(json_links)

for json_link in json_links:
    with urllib.request.urlopen(json_link) as url:
        data = json.loads(url.read().decode())
        if data['media']['assets']['ext' == "mp4"]:
            bin_links.append(data['media']['assets']['height' == "1080"]['url'])  # or 'height' == "720"
            video_names.append(data['media']['name'])
#print("Current Total links:",len(bin_links))
#print(bin_links)
#print(video_names)

## Formatea el nombre de tus videos.
video_names_f = []
for i in video_names:
    i = i.replace(".", "_", 1)
    i = re.sub(r"-.*?-", "_", i)
    video_names_f.append(i)
#print(video_names_f)

format = ".mp4"
for i in video_names_f:
    if format in i:
        video_namecheck.append(i)
    else:
        i += ".mp4"
        video_namecheck.append(i)
#print(video_namecheck)

n = 1
for i, j in zip(bin_links, video_namecheck):
    print("Downloading file "+str(n)+": " + str(j))
    (
        ffmpeg
        .input(str(i))
        .output(str(j), vcodec='copy', **{'loglevel': "panic"})
        .run()
    )
    #time.sleep(2)
    n +=1

print()
print("Download Complete, total videos:", n-1)
print()

## Optional
ans = input("""Optional: Would you like to I create folders for your files?
(y/n)?

""")
if ans == "y":
    link = input("""Please, give me the link of the MasterGIS website
where you're watching the videos.
For example: https://mastergis.teachable.com/courses/1073393/lectures/22874415
is the link for ArcGIS Curso Completo.
""")
    ## Get course title and section titles
    a = requests.get(link)
    soup = BeautifulSoup(a.content, 'html.parser')

    course_title = []
    for tag in soup.find_all("h2"):
            course_title.append(tag.text.strip())

    section_titles = []
    for tag in soup.find_all("div"):
        try: 
            tag['data-course-id']
            section_titles.append(tag.text.strip())
        except: continue

    section_titles_f = []       
    for title in section_titles:
        if title.startswith("Proyecto"):
            continue
        else:
            section_titles_f.append(title)
            
    #print(section_titles_f)
    #print(course_title[0])

    ## Create folders and move the respectives files
    if os.path.isdir(f'{course_title[0]}') is False:
        for i in  range(len(section_titles_f)):
            i+=1
            for j in glob.glob(f"{i}_*"):
                if os.path.isdir(f'{course_title[0]}/{i}_{section_titles_f[i-1]}') is False:
                    os.makedirs(f'{course_title[0]}/{i}_{section_titles_f[i-1]}')
                    shutil.move(j, f'{course_title[0]}/{i}_{section_titles_f[i-1]}')
                else:
                    shutil.move(j, f'{course_title[0]}/{i}_{section_titles_f[i-1]}')

    print()
    print("Folders created")
    print()
    print("Ty, program finished")
else:
    print()
    print("Ty, program finished")

